from __future__ import annotations

import json
import pathlib
import re
import sys
import traceback
from urllib.request import urlopen

import tomlkit


PYPI_METADATA_URL = 'https://pypi.org/pypi/{project_name}/json'
PROJECT_NAMES = ('ptpython', 'ipython')
VERSION_REGEX = re.compile(r'^(\d+)(?:\.(\d+))?(?:\.(\d+))?$')
PYPROJECT_TOML_PATH = pathlib.Path(__file__).parent / 'pyproject.toml'
HTTP_TIMEOUT = 30


Version = tuple[int, int, int]


def fetch_pypi_metadata(project_name) -> dict:
    url = PYPI_METADATA_URL.format(project_name=project_name)
    with urlopen(url, timeout=HTTP_TIMEOUT) as resp:
        return json.load(resp)


def load_pyproject_toml() -> tomlkit.TOMLDocument:
    with open(PYPROJECT_TOML_PATH, 'r') as fobj:
        return tomlkit.load(fobj)


def save_pyproject_toml(pyproject_toml: tomlkit.TOMLDocument) -> None:
    with open(PYPROJECT_TOML_PATH, 'w') as fobj:
        return tomlkit.dump(pyproject_toml, fobj)


def parse_version(version: str) -> Version:
    if not (match := VERSION_REGEX.fullmatch(version)):
        raise ValueError(f'cannot parse version: {version}')
    return tuple(map(lambda v: int(v) if v else 0, match.groups()))


def render_version(version: Version) -> str:
    return '.'.join(map(str, version))


def compare_versions(
    latest_versions: dict[str, Version], our_versions: dict[str, Version],
) -> int | None:
    part_needs_bump_index: int | None = None
    for project_name, latest_version in latest_versions.items():
        our_version = our_versions[project_name]
        if our_version >= latest_version:
            continue
        for part_index, (latest_part, our_part) in enumerate(
            zip(latest_version, our_version)
        ):
            if latest_part > our_part:
                if (
                    part_needs_bump_index is None
                    or part_needs_bump_index > part_index
                ):
                    part_needs_bump_index = part_index
                print(
                    (
                        f'need bump: {project_name} '
                        f'{our_version} -> {latest_version}'
                    ),
                    file=sys.stderr,
                )
                break
    return part_needs_bump_index


def bump_metapackage_version(
    metapackage_version: Version, part_needs_bump_index: int,
) -> Version:
    bumped_version = [0, 0, 0]
    for part_index, part in enumerate(metapackage_version):
        if part_index == part_needs_bump_index:
            bumped_version[part_index] = part + 1
            break
        bumped_version[part_index] = part
    return tuple(bumped_version)


def run():
    latest_versions: dict[str, Version] = {}
    for project_name in PROJECT_NAMES:
        pypi_metadata = fetch_pypi_metadata(project_name)
        latest_versions[project_name] = parse_version(
            pypi_metadata['info']['version'])

    our_versions: dict[str, Version] = {}
    pyproject_toml = load_pyproject_toml()
    for dependency in pyproject_toml['project']['dependencies']:
        project_name, _, raw_version = dependency.partition(' == ')
        our_versions[project_name] = parse_version(raw_version)

    part_needs_bump_index = compare_versions(latest_versions, our_versions)
    if part_needs_bump_index is None:
        print('versions are up-to-date, nothing to do', file=sys.stderr)
        return

    metapackage_version = parse_version(pyproject_toml['project']['version'])
    bumped_metapackage_version = bump_metapackage_version(
        metapackage_version, part_needs_bump_index)

    pyproject_toml['project']['version'] = render_version(
        bumped_metapackage_version)
    pyproject_toml['project']['dependencies'] = [
        f'{project_name} == {render_version(version)}'
        for project_name, version in latest_versions.items()
    ]
    save_pyproject_toml(pyproject_toml)

    print(f'version={render_version(bumped_metapackage_version)}')
    for project_name, version in latest_versions.items():
        print(f'{project_name}={render_version(version)}')


if __name__ == '__main__':
    try:
        run()
    except Exception:
        traceback.print_exc(file=sys.stderr)
