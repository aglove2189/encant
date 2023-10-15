import os

from encant import _extract, list, remove

test_path = os.path.dirname(__file__)
DEFAULT_OUTPUT_DIR = os.path.join(test_path, ".snakes")
sysname = "darwin"
machine = "aarch64"
TEST_VERSION = "3.10.13"


def test_add():
    path = os.path.join(
        test_path, "cpython-3.10.13+20231002-aarch64-apple-darwin-install_only.tar.gz"
    )
    with open(path, "rb") as f:
        obj = f.read()
        _extract(obj, TEST_VERSION, DEFAULT_OUTPUT_DIR)


def test_list(capsys):
    captured = capsys.readouterr()
    list()
    assert len(captured.out) == 1
    assert list()[0] == TEST_VERSION


def test_remove():
    remove(TEST_VERSION)
    assert len(list()) == 0
