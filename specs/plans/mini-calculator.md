# Implementation Plan: Mini Calculator (CLI)

## Overview
Build a single-file Python CLI calculator that adds two numbers, supports argument and interactive input, formats whole-number results without a trailing `.0`, and exposes `--help` via `argparse`. A companion test file verifies behavior with the standard-library `unittest` framework.

## Goals
- Create `calc.py` implementing all functional requirements from the spec.
- Support `--help` / `-h` via `argparse` and graceful error handling.
- Trim trailing `.0` from whole-number results using `float.is_integer()`.
- Cover behavior with unit and CLI-level tests using stdlib `unittest`.

## Scope
**In scope:** `calc.py`, `tests/test_calc.py`.
**Out of scope:** operations beyond addition, packaging, third-party dependencies (including pytest — tests use stdlib `unittest` to honor the spec's standard-library-only constraint).

## Prerequisites
- [ ] Python 3.8+ available (project venv exists at `.venv/`, Python 3.14).
- [ ] Spec read: `specs/0001-mini-calculator.md`.

## Implementation Steps

### Step 1: Implement the calculator CLI

Create the single-file calculator implementing input handling, argparse-based CLI, addition, result formatting, and error handling exactly as specified.

**Context:**
- See `specs/0001-mini-calculator.md` (Requirements, Technical Design)
- See `main.py` — existing placeholder script; the new tool lives in its own file (`calc.py`), not inside `main.py`.

**Actions:**
1. Create `calc.py` with a standard-library-only implementation:
   - Use `argparse` with two optional positional operands (nargs="?") so `--help` / `-h` work automatically and bad argument counts produce a usage error with non-zero exit.
   - When no operands are given, prompt interactively for each operand (stdin).
   - Parse operands as `float` (or int-aware equivalent); on `ValueError`, print a human-readable message including the invalid input to stderr and exit non-zero.
   - Compute the sum; format results with `float.is_integer()` so whole values print without a trailing `.0` (e.g. `2.0 + 3.0` → `5`) while fractional results keep their decimals.
   - Print the result to stdout and exit 0 on success.
2. Manually smoke-test the entry point:
   - Run: `python calc.py 2 3`
   - Run: `python calc.py --help`
   - Run: `python calc.py abc 1` (expect stderr error, non-zero exit)
   - Run: `python calc.py` with piped/typed interactive input.

**Success Criteria:**
- [ ] `calc.py` exists at the project root and imports only the standard library.
- [ ] `python calc.py 2 3` prints `5` to stdout and exits 0.
- [ ] `python calc.py 2.5 3` prints `5.5`; `python calc.py 1.5 2.5` prints `4` (no trailing `.0`).
- [ ] `python calc.py --help` and `python calc.py -h` print usage instructions and exit 0.
- [ ] Non-numeric input and wrong argument counts print an error to stderr and exit non-zero.

**Dependencies:** none

### Step 2: Add automated tests

Add unit tests for parsing/formatting logic and CLI-level tests for argument mode, interactive mode, help, and error cases.

**Context:**
- See `specs/0001-mini-calculator.md` (Testing Strategy)
- See `calc.py` (created in Step 1)

**Actions:**
1. Create `tests/test_calc.py` using stdlib `unittest` (no third-party test frameworks):
   - Unit-level: valid integers, valid floats, invalid strings, result formatting (whole vs fractional), missing/extra arguments.
   - CLI-level via `subprocess`: argument mode, interactive mode (piped stdin), `--help` / `-h` display, non-numeric input, wrong argument count.
   - Assert exit codes, stdout vs stderr routing (errors on stderr, results on stdout).
2. Run the suite:
   - Run: `python -m unittest discover -s tests -v`

**Success Criteria:**
- [ ] `tests/test_calc.py` exists and uses only `unittest` from the standard library.
- [ ] `python -m unittest discover -s tests -v` passes with all tests green.
- [ ] Tests cover: integer addition, float addition, whole-number formatting (no trailing `.0`), fractional formatting, `--help` / `-h`, non-numeric input error, wrong argument count error, interactive mode.
- [ ] Tests assert results go to stdout and errors go to stderr with correct exit codes.

**Dependencies:** 1

## Validation Checklist
- [ ] All functional requirements in `specs/0001-mini-calculator.md` are demonstrated by passing tests.
- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] No third-party dependencies introduced.
- [ ] `calc.py --help` output matches the tool's actual behavior.

## Risks and Mitigations
- **argparse interactive-mode conflict:** argparse treats unknown flags as errors and exits — verify no-args interactive path still works after argparse parsing (use optional positionals with `nargs="?"`).
- **Float formatting edge cases:** negative whole numbers and zero must also drop `.0`; covered by unit tests.
- **Stdlib-only testing:** `unittest` is less ergonomic than pytest — acceptable for this small suite.

## References
- Spec: `specs/0001-mini-calculator.md`
