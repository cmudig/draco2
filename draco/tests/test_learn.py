import json
from pathlib import Path

from draco.data_utils import pairs_to_vec
from draco.learn import train_model

root_path = Path(__file__).resolve().parents[2]
learn_data = {}

with open(root_path / "docs/applications/data/saket2018_draco2.json") as file:
    i = 0
    json_data = json.load(file)

    for pair in json_data:
        pair["source"] = "saket_2018"
        pair["pair_id"] = f'{pair["source"]}_{i}'
        learn_data[pair["pair_id"]] = pair
        i += 1

data = pairs_to_vec(learn_data)


def test_train_model():
    X = data.negative - data.positive
    clf = train_model(X, 0.3)

    non_zero_coef = 0
    for weight in clf.coef_[0]:
        if not weight == 0:
            non_zero_coef += 1

    assert not non_zero_coef == 0
