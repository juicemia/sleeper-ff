# Sleeper API Demo

## What Is This?

A little demo of what you can do with Sleeper's API.

The actual demo is an accurate calculation of best-ball points,
because Sleeper's current best-ball implementation is buggy.

## How Do I Run It?

```
# Make sure you have the Python version in `.python-version` installed.
pip install --upgrade virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Download the player database, you should only do this once per day:
curl "https://api.sleeper.app/v1/players/nfl" > players.json

./main.py --username MY_SLEEPER_USERNAME
```

Play around with the script and see what you can do.

API docs [here](https://docs.sleeper.app/#introduction).
