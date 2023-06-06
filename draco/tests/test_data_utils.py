import json
from pathlib import Path
from typing import DefaultDict

import pandas as pd

from draco import Draco
from draco.data_utils import count_preferences_memoized, pairs_to_vec, run_in_parallel

draco: Draco = Draco()
learn_data: dict[str, dict[str, str]] = {}

root_path: Path = Path(__file__).resolve().parents[2]
with open(root_path / "docs/applications/data/saket2018_draco2.json") as file:
    i: int = 0
    json_data: dict = json.load(file)

    for pair in json_data:
        pair["source"] = "saket_2018"
        pair["pair_id"] = f'{pair["source"]}_{i}'
        learn_data[pair["pair_id"]] = pair
        i += 1


def square(x: int) -> int:
    return int(x**2)


def batch_square(d: tuple[str, str, list[tuple[int, int]]]) -> pd.Series:
    _, _, xs = d

    s: pd.Series = pd.Series(dtype=int)
    for idx, x in xs:
        s = pd.concat([s, pd.Series([x**2], index=[idx])])
    return s


def test_run_in_parallel() -> None:
    a: list[int] = list(range(100))
    expected: list[int] = list(map(square, a))
    actual = run_in_parallel(batch_square, list(enumerate(a)), ("a", "b"))

    assert list(actual.values) == expected


def test_count_preferences_memoized() -> None:
    processed_specs: dict[str, DefaultDict[str, int]] = {}
    pair_id = "saket_2018_0"
    key = "saket_2018_0_negative"
    count_preferences_memoized(processed_specs, key, learn_data[pair_id]["negative"])
    assert key in processed_specs


def test_pairs_to_vecs() -> None:
    data: pd.DataFrame = pairs_to_vec(learn_data)

    assert set(data.negative.columns) == set(
        draco.soft_constraint_names
    ), "Feature names do not match."
