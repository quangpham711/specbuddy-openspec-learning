"""Mini CLI calculator that adds two numbers.

Supports:
  - Two positional operands via command-line arguments
  - Interactive prompting when no arguments are given
  - ``--help`` / ``-h`` via Python's built-in ``argparse``
  - Whole-number result formatting (e.g. ``2.0 + 3.0`` → ``5``)
  - Human-readable error messages on stderr with non-zero exit codes
  - A ``--gui`` flag opening a Tkinter desktop window
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


def calculate(first: float, second: float, subtract: bool) -> float:
    """Return *second* subtracted from *first* when *subtract*, else their sum."""
    return first - second if subtract else first + second


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
        "--gui",
        action="store_true",
        help="Open the calculator as a Tkinter desktop window.",
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

    if args.gui:
        return run_gui()

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
    result = calculate(first, second, args.subtract)
    print(format_result(result))
    return 0


def run_gui() -> int:
    """Open the calculator as a Tkinter desktop window; return the exit code."""
    try:
        import tkinter as tk
    except ImportError:
        print(
            "Error: the --gui flag requires Tkinter, which is not installed "
            "on this Python build. The command-line interface still works; "
            "run 'calc.py --help' for usage.",
            file=sys.stderr,
        )
        return 1

    root = tk.Tk()
    root.title("Calculator")

    first_var = tk.StringVar(root, value="")
    second_var = tk.StringVar(root, value="")
    operation = tk.StringVar(root, value="add")
    result_var = tk.StringVar(root, value="")
    error_var = tk.StringVar(root, value="")

    def _on_compute() -> None:
        error_var.set("")
        try:
            first = parse_operand(first_var.get())
            second = parse_operand(second_var.get())
        except ValueError as exc:
            error_var.set(str(exc))
            result_var.set("")
            return
        result_var.set(
            format_result(calculate(first, second, operation.get() == "subtract"))
        )

    tk.Label(root, text="Number 1:").grid(row=0, column=0, sticky="w", padx=4)
    first_entry = tk.Entry(root, textvariable=first_var)
    first_entry.grid(row=0, column=1, padx=4, pady=2, sticky="ew")

    tk.Label(root, text="Number 2:").grid(row=1, column=0, sticky="w", padx=4)
    second_entry = tk.Entry(root, textvariable=second_var)
    second_entry.grid(row=1, column=1, padx=4, pady=2, sticky="ew")

    tk.Label(root, text="Operation:").grid(row=2, column=0, sticky="w", padx=4)
    tk.Radiobutton(root, text="Add", variable=operation, value="add").grid(
        row=2, column=1, sticky="w"
    )
    tk.Radiobutton(root, text="Subtract", variable=operation, value="subtract").grid(
        row=2, column=2, sticky="w", padx=4
    )

    tk.Button(root, text="Compute", command=_on_compute).grid(
        row=3, column=1, pady=4
    )

    tk.Label(root, text="Result:").grid(row=4, column=0, sticky="w", padx=4)
    tk.Label(root, textvariable=result_var).grid(row=4, column=1, sticky="w")

    tk.Label(root, textvariable=error_var, fg="red").grid(
        row=5, column=0, columnspan=2, sticky="w", padx=4
    )

    root.grid_columnconfigure(1, weight=1)
    first_entry.bind("<Return>", lambda _event: _on_compute())
    second_entry.bind("<Return>", lambda _event: _on_compute())
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())