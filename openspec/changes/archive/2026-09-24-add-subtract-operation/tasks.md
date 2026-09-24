# Tasks

## 1. CLI Implementation

- [x] 1.1 Add a `--subtract` / `-s` `store_true` flag to `calc.py`'s argparse parser and update the parser `description` so `--help` mentions subtraction, then verify `python calc.py --help` shows the flag and both operations
- [x] 1.2 Wire the flag into `main()` so the tool computes `first - second` when set, then verify `python calc.py 5 3 --subtract` prints `2`, `python calc.py -s 5 7` prints `-2`, and both exit 0
- [x] 1.3 Confirm backward compatibility: verify `python calc.py 2 3` still prints `5` and `python calc.py 2.5 3` still prints `5.5`, both exiting 0, with no usage change
- [x] 1.4 Confirm interactive mode is unchanged, then verify `python calc.py` (piped operands via stdin) still prompts only for numbers, adds, and prints the sum

## 2. Automated Tests

- [x] 2.1 Add CLI-level tests to `tests/test_calc.py` covering `--subtract` after operands, `-s` before operands, and a negative difference, then verify `python -m unittest discover -s tests -v` passes
- [x] 2.2 Add a test covering the `--help` flag text now mentioning subtraction, then verify `python -m unittest discover -s tests -v` passes
- [x] 2.3 Ensure every existing addition scenario (argument mode, interactive mode, formatting, error cases) still passes, then verify `python -m unittest discover -s tests -v` is fully green

## 3. Validation

- [x] 3.1 Run the full suite `python -m unittest discover -s tests -v` and confirm all tests pass with exit code 0, demonstrating every requirement in `specs/mini-calculator/spec.md`