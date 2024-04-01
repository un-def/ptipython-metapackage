# ptipython metapackage

ptpython + ipython = ptipython

## Description

ptipython-metapackage is a convenient way to manage both [ptpython](https://github.com/prompt-toolkit/ptpython/) and [IPython](https://ipython.org/) as a single package. It brings not only both REPLs — `ptpython` and `ipython`, but in addition, `ptipython` — a combined “interactive shell with all the power that IPython has to offer” on top of ptpython features.

Unlike [alternatives](#alternatives), this metapackage uses pinned dependencies and tracks ptpython and IPython releases. Each time a new version of ptpython and/or IPython is released, there is a new version of ptipython-metapackage. It makes upgrading really easy — to get the latest versions of both ptpython and IPython you only need to upgrade the metapackage.

## Installation

ptipython-metapackage is built with [pipx](https://pipx.pypa.io/) in mind. To install the metapackage, run:

```shell
pipx install ptipython-metapackage
```

This command installs the latest version of the metapackage (that is, the latest versions of ptpython and IPython) and adds `ptpython`, `ipython`, and `ptipython` executables to `PATH`.

To upgrade to the latest version of the metapackage (that is, the latest version of ptpython and/or IPython), run:

```shell
pipx upgrade ptipython-metapackage
```

If you use `pip`, run

```shell
pip install -U ptipython-metapackage
```

to install or upgrade the metapackage.

## Alternatives

### Timo Furrer's [ptipython-meta](https://github.com/timofurrer/ptipython-meta)

```shell
pipx install --include-deps ptipython
```

### ptpython with `ptipython` extra

```shell
pipx install --include-deps 'ptpython[ptipython]'
```
