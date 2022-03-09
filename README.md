# Coin Metrics Community API Timeseries: Market Trades

## Objectives

1. Extract all trades for the `coinbase-btc-usd-spot` market for the past 24 hours.
2. Organize all trades by hour into separate `.csv` files.

## Technologies

| Required | Installation Link                                                        |
| -------- | ------------------------------------------------------------------------ |
| Python 3 | [python.org](https://www.python.org/downloads/)                          |
| Pip      | [pypi.org](https://pip.pypa.io/en/stable/installation/)                  |
| PipEnv   | [pipenv.pypa.io](https://pipenv.pypa.io/en/latest/#install-pipenv-today) |

## Instructions

There are some necessary dependencies that will need to be installed in order for this script to run. The most important of these is **Pipenv** which requires a version of Python 3 and Pip. If you do not have some of these technologies installed on your local machine, I have included links and additional instructions below.

1. Make sure you have installed all the required technologies necessary in order to run this project.

- Check your Python installation:

  > `python --version`

  - If you see an error, or your local version of Python is not a version of Python 3, please use the link in the [Technologies](#Technologies) table and follow the appropriate instructions to install a version of Python 3. Addtionally, you can follow Pipenv's guide to enure your Python and pip installation: [Pipenv guide](https://pipenv.pypa.io/en/latest/install/#make-sure-you-ve-got-python-pip)

- Check your Pip installation:
  > `pip --version`
  - Most versions of Python 3 will come with pip installed. However, if you see an error, pleaes follow the link in the [Technologies](#Technologies) table. Similarly to the last step, you can also go to Pipenv's guide for ensuring your Python and pip installation ([Pipenv guide](https://pipenv.pypa.io/en/latest/install/#make-sure-you-ve-got-python-pip))

2. Install all project dependencies with
   > `pipenv install`

- After you have installed pipenv, in your terminal, change into the directory for this script (directory name is 'timeseries-market-trades').

- Once you are in the proper directory, run the following command:

  > `pipenv install`

  - This will install all necessary project dependencies from the `Pipfile`.

- After pipenv finishes installing the project dependencies, run the following command in order to run the script:
  > `pipenv run python coinbase-btc-usd-spot.py`
  - This will create a directory names `timeseries` and generate all the files as per the objective.
  - After you run this script, you will see the status codes for each request being made being logged to the console.
  - For your convenience, after all the API requests have been made, the script will print the hour and the number of trades for each hour/file

## Additional Notes:

- After you run the script, there will be 25 files located in the `timeseries` directory.
  - Each file is prefixed with an `hour-XX` count where `XX` will be the division of hours (from 0 - 23) for the past day.
  - There is a 25th file `hour-24` that is generated as a safety in case the trade time does not fit into any of the previous divisions.
