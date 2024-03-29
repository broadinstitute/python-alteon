# pyalteon

This library provides a [Python][1] interface to the [Radware][2] [Alteon][6] REST API.  python-alteon is open sourced under the [BSD 3-Clause license](LICENSE.txt).

![checks](https://github.com/broadinstitute/python-alteon/workflows/checks/badge.svg?branch=main)

## Basics

pyalteon still runs on Python 2.7, and Python >= 3.4

## Features

## Installing

You can use pip to install pyalteon:

```sh
pipenv install pyalteon
```

## Examples

This is a simple example that just shows initializing the `Client` object and using it to query the `Organization` and `SSL` endpoints:

```python
from pyalteon import Client

client = Client(
    hostname="vadc.example.org",
    username="your_username",
    password="your_password",
)
```

## Contributing

Pull requests to add functionality and fix bugs are always welcome.  Please check the CONTRIBUTING.md for specifics on contributions.

### Testing

We try to have a high level of test coverage on the code.  Therefore, when adding anything to the repo, tests should be written to test a new feature or to test a bug fix so that there won't be a regression.  This library is setup to be pretty simple to build a working development environment using [Docker][4].  Therefore, it is suggested that you have [Docker][4] installed where you clone this repository to make development easier.

To start a development environment, you should be able to just run the `dev.sh` script.  This script will use the `Dockerfile` in this repository to build a [Docker][4] container with all the dependencies for development installed using [Poetry][3].

```sh
./dev.sh
```

The first time you run the script, it should build the [Docker][4] image and then drop you into the container's shell.  The directory where you cloned this repository should be volume mounted in to `/usr/src`, which should also be the current working directory.  From there, you can make changes as you see fit.  Tests can be run from the `/usr/src` directory by simply typing `green` as [green][5] has been setup to with the correct parameters.

[1]: https://www.python.org/ "Python"
[2]: https://www.radware.com/ "Radware"
[3]: https://python-poetry.org/ "Poetry"
[4]: https://www.docker.com/ "Docker"
[5]: https://github.com/CleanCut/green "green"
[6]: https://www.radware.com/products/alteon/ "Alteon"
