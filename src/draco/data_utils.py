import logging
import math
from multiprocessing import Manager, cpu_count
from typing import Any, DefaultDict, Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
from pandas.util import hash_pandas_object

from .draco import Draco

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

draco = Draco()


def get_nested_index(fields: Tuple[str, str] = ("negative", "positive")):
    """
    Gives you a nested pandas index that we apply to the data when creating a dataframe.
    """
    feature_names: List[str] = draco.soft_constraint_names
    iterables: List[List | Tuple] = [fields, feature_names]
    index: pd.MultiIndex = pd.MultiIndex.from_product(
        iterables, names=["category", "feature"]
    )
    index = index.append(pd.MultiIndex.from_arrays([["source", "task"], ["", ""]]))
    return index


def run_in_parallel(
    func,
    data: List,
    fields: Tuple[str, str] = ("negative", "positive"),
) -> pd.DataFrame:
    """Like map, but parallel."""

    splits = min([cpu_count() * 20, math.ceil(len(data) / 10)])
    df_split: List = np.array_split(data, splits)
    processes = min(cpu_count(), splits)

    logger.info(
        f"Running {splits} partitions of {len(data)} items "
        "in parallel on {processes} processes."
    )

    with Manager() as manager:
        m: Any = manager  # fix for mypy
        d = m.dict()  # shared dict for memoization
        pool = m.Pool(processes=processes)

        tuples: List[Tuple[Dict, Tuple[str, str], Any]] = []
        for s in df_split:
            # add some arguments
            tuples.append((d, fields, s))

        df = pd.concat(pool.map(func, tuples))
        pool.close()
        pool.join()

    df = df.sort_index()

    logger.info(f"Hash of dataframe: {hash_pandas_object(df).sum()}")

    return df


def pair_partition_to_vec(
    input_data: Tuple[
        Dict,
        Tuple[str, str],
        List[Dict],
    ],
):
    """given a specs partition, convert them into feature vectors."""
    processed_specs, fields, partition_data = input_data

    columns = get_nested_index()
    dfs = []

    for example in partition_data:
        neg_feature_vec = count_preferences_memoized(
            processed_specs, f"{example['pair_id']}_{fields[0]}", example[fields[0]]
        )

        pos_feature_vec = count_preferences_memoized(
            processed_specs, f"{example['pair_id']}_{fields[1]}", example[fields[1]]
        )

        # Reformat the json data so that we can insert it into a multi index data frame.
        # https://stackoverflow.com/questions/24988131/nested-dictionary-to-multiindex-dataframe-where-dictionary-keys-are-column-label
        feature_vecs = {
            (fields[0], key): values for key, values in neg_feature_vec.items()
        }
        feature_vecs.update(
            {(fields[1], key): values for key, values in pos_feature_vec.items()}
        )

        feature_vecs[("source", "")] = example["source"]
        feature_vecs[("task", "")] = example["task"]

        dfs.append(
            pd.DataFrame(feature_vecs, columns=columns, index=[example["pair_id"]])
        )

    return pd.concat(dfs).fillna(0)


def count_preferences_memoized(
    processed_specs: Dict[str, DefaultDict[str, int]],
    key: str,
    spec: str | Iterable[str],
) -> DefaultDict[str, int]:
    """
    count preferences if the example's violations hasn't been counted
    by other processes.
    """

    if key not in processed_specs:
        violations = draco.count_preferences(spec)
        if violations is not None:
            processed_specs[key] = violations
    return processed_specs[key]


def pairs_to_vec(
    specs: Dict[str, Dict], fields: Tuple[str, str] = ("negative", "positive")
) -> pd.DataFrame:
    """
    Given pairs of positive and negative Draco specifications, count the number of times
    each preference is violated. The input pairs are partitioned so that
    ``count_preferences_memoized`` can run parallelly by multiple processes.

    :return: A Dataframe indexed by the pair ids that can be used to train draco-learn.
            It can have the following columns:

    * ``source``: The collection that the pair is from.
    * ``task``: What task does the pair perform.
    * ``(field, feature)``: the ``field`` indicates if it's the positive or negative
                            example of the pair, and the ``feature``
                            refers to the preference.
                            The value is the count of preference violations.
    """

    return run_in_parallel(pair_partition_to_vec, list(specs.values()), fields)
