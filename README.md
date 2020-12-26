# Advent of Code 2020
Here are my solutions to the [Advent of Code 2020](https://adventofcode.com/2020) puzzles.

The puzzles for each day are stored in separate directories. There is an extra
directory to split solutions by language. I'm doing all solutions in Python and
Go.

## Running the solutions
To run one of the solutions, simply follow best practices for each language. All
puzzles expect input from stdin. The input provided by Advent of Code is stored
in a file named `input.txt` at the root of each puzzle directory.
Each solution will expect a parameter, whose value can be `one` or `two`. This
will tell the code to solve the problem as the first or the second part of the
puzzle for that day.

To read the definition for each problem, please visit the Advent of Code
website.
I will do my best to avoid any external dependencies. All solutions will include
unit tests.

### Example: Python
```
# run puzzle for part one of day one
cd 01/python
cat ../input.txt | add_2020.py one

# run test
cd 01/python
python3 -m unittest autodiscover
# - or -
cd 01/python
python3 test_add_2020.py
```

### Example: Go
```
# run puzzle for part two of day one
cd 01/go
go build add_2020.go
cat ../input.txt | add_2020 two

# run test
cd 01/go
go test

# delete artefacts
cd 01/go
go clean
```

## Development
To enforce correctness and code style, please enable the githook like this:
```
git config --local core.hooksPath .githooks/
```

This hook will enforce code style by automatically applying changes and it will
run a few linters and the associated unit tests before storing your commit.

Requirements:
* pylint
* autopep8
* mypy
