import pytest

from checker import compare_versions


LATEST_VERSIONS = {'ptpython': (3, 0, 26), 'ipython': (8, 22, 2)}


@pytest.mark.parametrize(['our_versions', 'expected'], [
    ({'ptpython': (3, 0, 26), 'ipython': (8, 22, 2)}, None),
    ({'ptpython': (4, 0, 0), 'ipython': (8, 22, 2)}, None),
    ({'ptpython': (4, 0, 0), 'ipython': (9, 0, 0)}, None),
    ({'ptpython': (4, 0, 0), 'ipython': (8, 22, 0)}, 2),
    ({'ptpython': (3, 0, 25), 'ipython': (8, 22, 1)}, 2),
    ({'ptpython': (3, 0, 25), 'ipython': (8, 21, 0)}, 1),
    ({'ptpython': (2, 1, 28), 'ipython': (8, 21, 0)}, 0),
    ({'ptpython': (3, 0, 0), 'ipython': (7, 34, 1)}, 0),
])
def test(our_versions, expected):
    assert compare_versions(LATEST_VERSIONS, our_versions) == expected
