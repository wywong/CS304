CPSC 304
========

Setup
=====

Make sure you have the appropriate MySQL packages installed.

Get `python-pip` and `python-virtualenv`

Set up the virtual environment.

`virtualenv env`

`. env/bin/activate`

Install packages by running: `pip install -r requirements.txt`

Create a file `database.cfg` containing `host`, `username`, `password`, and the `database name`.

For example:
```
localhost
testuser
01189998819991197253
cs304
```

Set up the appropriate tables by running: `python setup.py`

To run `python site.py`

Open `localhost:5000` in the web browser of your choice.

Contributors
============

[Evan J. Friday](https://github.com/EvanFriday)

[Shibo M. Weng](https://github.com/SMWTLM)

[Wilson Y. Wong](https://github.com/wywong)
