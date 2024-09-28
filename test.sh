#!/bin/bash

poetry run pytest --cov-report term-missing --cov-report xml --cov-report html --cov expense_tracker tests/
