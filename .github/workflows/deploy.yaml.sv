---
name: 'deploy'

'on':
  push:
    tags:
      - '[0-9]+.[0-9]+.[0-9]+'

jobs:
  pypi_deploy:

    runs-on: 'ubuntu-latest'

    steps:
      - name: 'Checkout repo'
        uses: 'actions/checkout@v3'

      - name: Install poetry
        run: pipx install poetry

      - name: 'Set up Python 3.10'
        uses: actions/setup-python@v4
        with:
          cache: 'poetry'
          python-version: '3.10'

      - name: 'Configure Poetry'
        run: 'poetry config virtualenvs.in-project true'

      - name: 'Install dependencies'
        run: 'poetry install'

      - name: 'Setup PyPi credential'
        env:
          PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
        run: 'poetry config pypi-token.pypi "$PYPI_TOKEN"'

      - name: 'Package build'
        run: 'poetry build'

      - name: 'Publish package to PyPi'
        run: 'poetry publish'
