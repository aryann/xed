# Development

## Uploading to PyPI

### Prerequisites

First, make sure all of the required tools are installed and up-to-date:

```
python -m pip install --user --upgrade setuptools wheel twine
```

Then build and upload the artifacts by running these commands from the repo's
base directory:

```
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```
