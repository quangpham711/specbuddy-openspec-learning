# Design

## Context

`calc.py` (89 lines) is a single-file, stdlib-only Python calculator. `main()` parses `--subtract`/`-s` and up to two positional operands, prompts interactively (to stderr) for missing operands, prints `format_result(first ∓ second)` to stdout, and returns an int exit code (`calc.py:30-85`). The arithmetic is currently inlined at `calc.py:83`. Both `parse_operand()` and `format_result()` are pure and already unit-tested. Tkinter 8.6 is available on this machine. The change adds a `--gui` flag that opens a simple form-based window (see `proposal.md` — Why/What Changes).

## Goals / Non-Goals

**Goals:**
- `calc.py 2 3`, `-s`, interactive prompts, error messages, and exit codes are byte-for-byte unchanged when `--gui` is absent.
- The GUI reuses `parse_operand`, `format_result`, and one shared `calculate()` helper — no duplicated arithmetic or formatting.
- `tkinter` is imported lazily so the CLI runs on Python builds without Tk.
- The file stays single-file and stdlib-only.

**Non-Goals:**
- No new operations, keypad, or arithmetic-expression evaluation (multiplication/division remain out of scope).
- No dedicated widget-level GUI test suite that requires a display server (see Risks).
- No auto-launching the GUI when `--gui` is absent — interactive prompting stays the no-argument behavior.

## Decisions

### `--gui` is a store_true argparse flag that takes precedence over operands
`main()` gains a `--gui` flag. If present, the function opens the GUI and ignores any positional operands rather than computing them; the flag is explicit and documentable in `--help`. Alternative considered: a separate `calc_gui.py`. Rejected because the capability's purpose is a single-file tool and Option A keeps the CLI untouched unless the flag is passed; `calc_gui.py` would fragment the project into two files for no behavior win. Alternative considered: auto-open GUI when stdout is not a TTY — rejected because no-argument invocation is spec-bound to interactive prompting.

### Shared `calculate(first, second, subtract) -> float`
Extract the arithmetic at `calc.py:83` into a module-level pure function:

```
def calculate(first: float, second: float, subtract: bool) -> float:
    return first - second if subtract else first + second
```

`main()` calls it for the CLI path; the GUI's Compute handler calls the same function. This gives one testable math surface shared by both interfaces.

### GUI layout and Compute flow
`run_gui()` is a self-contained function that constructs a `tk.Tk` root with a grid layout:

```
+------------------------------------------+
|  Number 1: [_______________]              |
|  Number 2: [_______________]              |
|  Operation: (o) Add   ( ) Subtract        |
|            [ Compute ]                    |
|  Result:   ____________                   |
|  Error:    ____________ (red text)          |
+------------------------------------------+
```

- Two `tk.Entry` widgets bound to `StringVar`s (default `""`).
- A `StringVar` bound to two `tk.Radiobutton`s, `"add"`/`"subtract"`, defaulting to `"add"`.
- A Compute `tk.Button` triggering `_on_compute()`.
- A result `StringVar` label and an error `StringVar` label (red foreground, default empty).
- `_on_compute()` parses both entries via `parse_operand`. On `ValueError`, sets the error label (message already includes the invalid input, e.g. `Invalid number: 'abc'`) and clears the result; on success, sets the result label via `calculate()` + `format_result()` and clears the error. The window stays open after computing (`mainloop()` continues).
- Return-key binding on the entries triggers Compute for keyboard users.

### Lazy tkinter import with graceful failure
`import tkinter` happens inside `run_gui()` only. If it raises `ImportError`, `run_gui()` prints a clear message to stderr (including that the CLI still works) and returns a non-zero exit code, satisfying the spec scenario. The CLI path never imports tkinter.

### Help text
`parser.add_argument("--gui", action="store_true", help="Open the calculator as a Tkinter desktop window.")` — appears in `--help` naturally; no manual help formatting. Existing help assertions (subtraction text) remain satisfied.

## Risks / Trade-offs

- **Tk not installed on minimal Python builds** → Mitigated by the lazy import and the clear stderr error; the CLI and all its tests run without Tk. This project's spec and tests remain display-free.
- **Widget-level behavior is hard to test without a display** → Mitigated by pushing all behavior into `parse_operand`/`format_result`/`calculate` (covered by unit tests in any environment) and keeping `_on_compute()` a thin glue layer. Scenario coverage is asserted by a small direct test of `run_gui()`'s logic only where a display is available; the default test run stays headless.
- **`--gui` with extra positional operands is silently ignored** → Recorded design decision: the flag takes precedence, documented in `--help` ("opens a window"). Prevents surprising errors while keeping the CLI form unchanged.
- **Argparse `--help` output changes** (adds `--gui` line) → Additive only; the spec requires help to mention subtraction, which it still does.

## Migration Plan

Deploy as a normal edit to `calc.py` and `tests/test_calc.py`. The change is additive and backward compatible — every existing invocation behaves identically. Rollback is a single revert of both file diffs. No data, configuration, or external systems are involved.

## Open Questions

None — decisions above resolve every choice that would otherwise change the specs, the approach, or the task breakdown.