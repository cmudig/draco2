from draco import dict_union


def test_dict_union():
    assert dict_union({"foo": 12}, {"bar": 7}) == {"foo": 12, "bar": 7}
    assert dict_union({"foo": 12}, {"foo": 42, "bar": 7}) == {"foo": 42, "bar": 7}
