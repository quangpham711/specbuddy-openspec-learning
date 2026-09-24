# Design

## Context

The change adds subtraction to the existing single-file, standard-library-only Python CLI (`calc.py`). The current `main()` uses `argparse`, collects up to two operands (positional, `nargs="*"`, falls back to interactive prompts via stdin when short), always computes `first + second`, and formats the result with `format_result()` (drops trailing `.0` for whole numbers). Errors go to stderr with a non-zero exit. There are no third-party dependencies and the project is a small practice app (see `proposal.md` for motivation). OpenSpec currently has no declared capabilities; this change introduces the `mini-calculator` capability.

## Goals / Non-Goals

**Goals:**
- Add subtraction without a new positional argument or subcommand so existing invocations keep their meaning.
- Keep the change to `calc.py` and `tests/test_calc.py` only; no new dependencies.
- Reuse the existing operand parsing, result formatting, and error routing unchanged.

**Non-Goals:**
- No operation prompt in interactive mode (it stays addition-only).
- No multiplication, division, operator-precedence parsing, or arithmetic expression evaluation.
- No rearchitecting the CLI (no subparsers, no operator argument).

## Decisions

### Subtraction is selected by a boolean flag, `--subtract` / `-s`, defaulting to off
`argparse` gains one flag (`store_true`). When set, `main()` computes `first - second`; when unset it computes `first + second` as today.

Rationale: a flag leaves the positional signature untouched, so `calc.py 2 3` is byte-for-byte backward compatible. Alternatives considered:
- **Operation word / subcommands** (`calc.py sub 5 3`): clearer about intent, but **breaking** — existing `calc.py 5 3` invocations would change meaning and the spec's existing scenarios depend on the two-number form.
- **Operator symbol argument** (`calc.py 5 - 3`): `argparse` treats a lone `-` awkwardly and it reads ambiguously with negative operands.
- **`--operation add|sub` valued flag**: more verbose than a boolean flag for a two-operation tool; `--subtract` is self-documenting.

### Interactive mode always adds
Interactive prompts collect only operands; the operation is never prompted for. A flag is non-idiomatic as a stdin answer, and the default must stay addition to preserve the existing interactive behavior. Users wanting subtraction pass the flag plus both operands on the command line.

### Message host-signing … `format_result` is reused as-is
Subtraction results flow through the same `format_result` path, so `5 7 --subtract → -2` and fractional differences format identically to sums. Negative whole numbers (e.g. `-2`) already handled by `float.is_integer()`.

### Argparse description text updated
`description="Add two numbers."` becomes text covering both operations, and the flag's `help` mentions `-s`. This keeps `--help` accurate (the spec requires help to mention subtraction).

## Risks / Trade-offs

- **`-s` short-flag collision** → Currently only `-h` exists, so no collision. If future operations add short flags, revisit the character set before all of them are "taken." Mitigated by the boolean-flag design being easy to extend.
- **Flag order flexibility** → `--subtract` may appear before or after operands; `argparse` handles this, but tests should cover one representative order (after operands) plus the short-form-before-operands case to pin behavior.
- **Interactive + flag ambiguity** → If a user passes `-s` with no operands, `main()` will prompt for operands then still subtract, which may look surprising. Documented decision: interactive prompts only supply operands; the operation comes solely from the flag.
- **Spec duplication** → The OpenSpec delta describes the entire calculator behavior (existing addition plus new subtraction) because the capability is new to OpenSpec. The project's `specs/0001-mini-calculator.md` file is a separate spec-system artifact and is not modified as part of this change.

## Migration Plan

Deploy as a normal edit to `calc.py`; the change is additive and backward compatible (`calc.py 2 3` output is unchanged). Rollback is a single revert of the `calc.py` and `tests/test_calc.py` diffs. No data, configuration, or external systems are involved.

## Open Questions

None — decisions above resolve every choice that would otherwise change the specs or task breakdown.