# Proposal

## Why

The mini calculator CLI currently only supports addition. Subtracting one number from another is a basic arithmetic need users expect from a calculator, and adding it makes the tool useful beyond its single-operation prototype without trading away backward compatibility.

## What Changes

- Add a `--subtract` / `-s` flag to `calc.py` that performs subtraction instead of the default addition.
- Keep the existing two-number invocation (`calc.py 2 3`) meaning addition — fully backward compatible.
- Examples after the change:
  - `calc.py 2 3` → `5` (unchanged, addition)
  - `calc.py 5 3 --subtract` → `2`
  - `calc.py -s 5 3` → `2`
- Interactive mode continues to default to addition; no operation prompt is added.
- Reuse the existing `format_result` logic as-is so negative and fractional results format consistently (e.g. `calc.py 5 7 --subtract` → `-2`).
- Update the argparse `description` and `--help` text to describe both operations.
- Add unit and CLI-level tests covering `--subtract` / `-s` in both argument and no-argument modes.

## Capabilities

### New Capabilities
- `mini-calculator`: the CLI calculator capability covering two-operand input (command-line arguments or interactive prompting), whole-number result formatting, and the two supported operations — addition by default and subtraction via `--subtract` / `-s`.

### Modified Capabilities
<!-- No existing OpenSpec specs; the calculator was never declared as an OpenSpec capability. -->

## Impact

- `calc.py` — CLI surface and `main()` gain the subtract flag; no new dependencies, stdlib only.
- `tests/test_calc.py` — new unit and CLI tests for the subtract flag and updated help text.
- `--help` output changes (argparse description and flag listing).
- Note: `specs/0001-mini-calculator.md` (a separate spec-system file, not an OpenSpec spec) lists subtraction among its non-goals; that scope note is superseded for subtraction by this change but the file itself is not an OpenSpec delta target.