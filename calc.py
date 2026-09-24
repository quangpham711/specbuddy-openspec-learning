"""Mini CLI calculator that adds two numbers.

Supports:
  - Two positional operands via command-line arguments
  - Interactive prompting when no arguments are given
  - ``--help`` / ``-h`` via Python's built-in ``argparse``
  - Whole-number result formatting (e.g. ``2.0 + 3.0`` → ``5``)
  - Human-readable error messages on stderr with non-zero exit codes
"""

import argparse
import sys


def parse_operand(value: str) -> float:
    """Convert *value* to a number; raise ``ValueError`` on failure."""
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"Invalid number: '{value}'") from exc


def format_result(result: float) -> str:
    """Format *result* without a trailing ``.0`` when it is a whole number."""
    if result.is_integer():
        return str(int(result))
    return str(result)


def main(argv: list[str] | None = None) -> int:
    """Entry point for the calculator CLI."""
    parser = argparse.ArgumentParser(
        prog="calc.py",
        description="Add or subtract two numbers.",
    )
    parser.add_argument(
        "-s",
        "--subtract",
        action="store_true",
        help="Subtract the second number from the first instead of adding.",
    )
    parser.add_argument(
        "operands",
        metavar="NUMBER",
        type=str,
        nargs="*",
        default=[],
        help="Optional numbers; use two for immediate calculation or fewer to "
             "be prompted interactively.",
    )
    args = parser.parse_args(argv)

    # Too many operands is an error.
    if len(args.operands) > 2:
        print("Error: at most two operands allowed.", file=sys.stderr)
        return 1

    operands: list[float] = []

    # Collect the operands we were given on the command line.
    for s in args.operands:
        try:
            operands.append(parse_operand(s))
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 1

    # Prompt interactively for any missing operands, writing the prompt
    # to stderr so stdout remains clean for the result.
    while len(operands) < 2:
        try:
            print("Enter number: ", file=sys.stderr)
            value = input()
        except EOFError:
            return 1
        try:
            operands.append(parse_operand(value))
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 1

    first, second = operands[0], operands[1]
    result = first - second if args.subtract else first + second
    print(format_result(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())