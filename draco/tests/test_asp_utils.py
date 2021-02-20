from pathlib import Path

import pytest
from draco.asp_utils import Block, blocks_to_program, parse_blocks

VALID_CONTENT = """
some content to ignore

% @test(foo) some description
fact1.

% @test(bar) some description
fact2.

"""


@pytest.fixture(scope="session")
def asp_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test.asp")
    with open(filename, "w") as f:
        f.write(VALID_CONTENT)
    return Path(filename)


def test_parse_blocks(asp_file):
    assert parse_blocks(asp_file) == {
        "__preamble__": "some content to ignore\n",
        "foo": Block("test", "some description", "fact1.\n"),
        "bar": Block("test", "some description", "fact2.\n"),
    }


@pytest.fixture(scope="session")
def empty_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test.asp")
    with open(filename, "w") as f:
        f.write("")
    return Path(filename)


def test_parse_empty_file(empty_file):
    assert parse_blocks(empty_file) == {}


def test_blocks_to_program(asp_file):
    blocks = parse_blocks(asp_file)
    program = blocks_to_program(blocks)

    assert program == ["fact1.\n", "fact2.\n"]
