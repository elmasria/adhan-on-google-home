# ADHAN On Google Home
Listen to adhan on google home speakers

[![codecov](https://codecov.io/gh/elmasria/adhan-on-google-home/branch/main/graph/badge.svg?token=F0ZP5R7LR1)](https://codecov.io/gh/elmasria/adhan-on-google-home)

## Overview

The app will help run the Adhan based on the mosque you specify.

## Getting Started

### Prerequisites

- Python (3.10 or newer)
- poetry
    ```sh
    curl -sSL https://install.python-poetry.org | python -
    ```
### Installation

- Activate the virtual environment
    ```sh
    poetry shell
    ```
- Install dependencies
    ```sh
    poetry install
    ```
- Add .env variables
    ```sh
    MAWAQIT_USERNAME=example@mail.com
    MAWAQIT_PASSWORD="YOUR_PASSWORD"
    ```
## Usage

### Directly on your pc

```sh
poe start
```

## Running the tests

```sh
poe test
```

## Reference

- [poetry](https://python-poetry.org/docs/)
- [Mawaqit](https://mawaqit.net/)

## License

[LICENSE](LICENSE)