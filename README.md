# encant: Uber Simple Python Version Management

----
[![image](https://img.shields.io/pypi/v/encant.svg)](https://pypi.python.org/pypi/encant)

Built in spite of [pyenv](https://github.com/pyenv/pyenv) and inspired by [rye](https://github.com/mitsuhiko/rye), encant does one thing and one thing only: downloads standalone python builds. Builds come from indygreg's [repo](https://github.com/indygreg/python-build-standalone).

## Usage

install encant

```bash
pipx install encant
```

install a python version (or two)

```bash
$ encant 3.10
major.minor only version detected, pulling latest: 3.10.13
3.10.13 written to /Users/aaron/.snakes/3.10.13
```

That's it! You can now use python however you need to, e.g.:

```bash
$HOME/.snakes/3.10.13/bin/python3 -m venv .venv
```
