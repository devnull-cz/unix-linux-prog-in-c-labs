# Testing

Python 3.x is needed to run these tests.
The tests assume that the `mqttserver` binary is available in the parent directory.

To run the tests by hand, use these steps:

```
python3 -m venv venv
. ./venv/bin/activate
python3 -m pip install -r requirements.txt
pytest
```

or to run an individual test (assuming activated Python virtual environment):
```
pytest functional/test_keepalive.py
```

## Tracking changes

Each group of tests is versioned. The version is embedded in the respective
`__init__.py` file for each Python package, e.g. `functional/__init__.py`
contains the `VERSION` variable.

The `VERSION` value is bumped for each non-trivial change.

Always make sure you have the latest tests.

Also, it does not hurt to update the packages in the Python virtual environment once in a while:
```
python3 -m pip install --upgrade -r requirements.txt
```

## Github Actions

You can set up your Github repository so that the tests run via Github action on push.
Here is sample configuration that can be placed in the `.github/workflows/build.yml` file in the Git repository
to make this work:
```yml
name: Build

on:
  push:
    paths-ignore:
    - README.md

jobs:
  build:
    name: ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest]
    steps:
    - name: Checkout master branch
      uses: actions/checkout@v4
    - name: build
      run: make
    - uses: actions/setup-python@v5
      with:
        python-version: "3.10"
    - name: Install test dependencies
      working-directory: tests
      run: |
        pip install -r requirements.txt
    - name: Run tests
      working-directory: tests
      run: pytest
```
