# Proposal

## Why

The calculator is currently CLI-only, which requires a terminal. A simple Tkinter GUI makes the same two operations available to users who prefer a windowed interface, and Tkinter is part of the Python standard library, so the project keeps its no-third-party-dependencies constraint.

## What Changes

- Add a `--gui` flag to `calc.py` that opens a Tkinter window; without it the CLI behaves exactly as today.
- The GUI is form-based: two numeric entry fields, an Add/Subtract operation selection, a Compute button, a result display, and inline error messages.
- The GUI reuses the existing `parse_operand` and `format_result` logic and a newly extracted `calculate(first, second, subtract)` helper, so parsing, error wording, and result formatting match the CLI exactly with no duplication.
- Lazy-import `tkinter` inside the GUI path only, so the CLI keeps working on Python builds without Tk installed.
- `--help` / `-h` output gains a `--gui` line; all existing help, error, exit-code, and interactive-prompt scenarios stay satisfied.
- Add tests for the extracted `calculate` helper so the shared math is exercised directly; existing CLI tests remain unchanged and passing.

## Capabilities

### New Capabilities
<!-- None — the GUI is an extension of the existing single calculator tool. -->

### Modified Capabilities
- `mini-calculator`: gains a GUI-mode requirement — running `calc.py --gui` opens a form with two operand inputs, Add/Subtract selection, a Compute button, a formatted result, and inline errors, while the existing CLI requirements (including interactive prompting when `--gui` is absent) remain unchanged.

## Impact

- `calc.py` — modifies `main()` (adds `--gui`), extracts a shared `calculate()` helper, and adds a `run_gui()` function; the file stays single-file.
- `tests/test_calc.py` — adds tests for `calculate()` and the `--gui` flag; existing tests unchanged.
- `--help` output changes (adds the `--gui` flag listing).
- No new dependencies — Tkinter is stdlib. Tk must be present for the GUI path; on systems without it, `calc.py --gui` reports a clear error while the CLI remains fully usable.