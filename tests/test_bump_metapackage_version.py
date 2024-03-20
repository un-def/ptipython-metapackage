import pytest

from checker import bump_metapackage_version


@pytest.mark.parametrize(['metapackage_version', 'part_index', 'expected'], [
    ((1, 6, 11), 0, (2, 0, 0)),
    ((1, 6, 11), 1, (1, 7, 0)),
    ((1, 6, 11), 2, (1, 6, 12)),
])
def test(metapackage_version, part_index, expected):
    assert bump_metapackage_version(
        metapackage_version, part_index) == expected
