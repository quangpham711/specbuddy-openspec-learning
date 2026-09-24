# Tasks

## 1. Shared calculation core

- [x] 1.1 Add a module-level `calculate(first: float, second: float, subtract: bool) -> float` helper to `calc.py` that returns `first - second` when `subtract` is true and `first + second` otherwise, and refactor `main()` to call it instead of the inline arithmetic at `calc.py:83`. Verify `python -m unittest discover -s tests` still passes all 23 existing tests unchanged.
- [x] 1.2 Add unit tests for `calculate()` covering add, subtract, negative difference, and fractional difference (mirroring `format_result` expectations in `tests/test_calc.py`). Verify the new tests pass under `python -m unittest discover -s tests`.

## 2. `--gui` flag and CLI dispatch

- [x] 2.1 Add a `--gui` store_true flag to the argparse parser in `main()` (with help text describing the desktop window), and dispatch to `run_gui()` immediately after parsing when the flag is present, ignoring positional operands. Verify `python calc.py --help` lists `--gui` and `python calc.py 2 3` still prints `5`.
- [x] 2.2 Add a CLI test asserting `--help` output mentions `--gui` (extend the existing `--help` tests in `tests/test_calc.py`). Verify the suite passes.

## 3. Tkinter GUI

- [x] 3.1 Implement `run_gui()` with a lazy `import tkinter` inside the function; build a `tk.Tk` window with two `tk.Entry` fields bound to `StringVar`s, two `tk.Radiobutton`s bound to an operation `StringVar` (Add default, Subtract), a Compute `tk.Button`, a result `StringVar` label, and a red error `StringVar` label. Verify the window opens with `python calc.py --gui` on a machine with Tk and shows all widgets.
- [x] 3.2 Implement the Compute handler `_on_compute()`: parse both entries via `parse_operand` (showing the `ValueError` message in the error label and clearing the result on failure), otherwise compute via `calculate()` + `format_result()` and display it, keeping the window open. Verify manual entry of `2`/`3` Add shows `5`, `5`/`3` Subtract shows `2`, `2.0`/`3.0` shows `5`, and `abc`/`3` shows the inline error and no result.
- [x] 3.3 Bind the Return key on both entries to trigger Compute. Verify pressing Enter in either field computes.
- [x] 3.4 Make `run_gui()` handle a missing Tk: catch the tkinter `ImportError`, print a clear error naming `--gui` and noting the CLI still works to stderr, and return a non-zero exit code. Verify with a unit test that patches import of `tkinter` to raise `ImportError` and asserts `main()` (with `sys.argv = ["calc.py", "--gui"]`) returns non-zero and writes the message to stderr, and that the non-`--gui` path never imports tkinter.

## 4. Regression verification

- [x] 4.1 Run the full suite with `python -m unittest discover -s tests` and confirm all existing CLI, format, parse, and new `calculate`/`--gui` tests pass.
- [x] 4.2 Manually verify CLI parity: `python calc.py 2 3` prints `5`, `python calc.py 5 3 --subtract` prints `2`, `python calc.py abc 1` errors to stderr with non-zero exit, and `python calc.py` (no args) still prompts interactively with stdout `5`.