# Mini Calculator (CLI)

## Overview
Specification for a simple Python command-line calculator that performs addition of two numbers.

## Goals
- Provide a working Python CLI tool for adding two numbers.
- Accept input interactively or as command-line arguments.
- Return clear, readable output and handle invalid input gracefully.

## Non-Goals
- Operations beyond addition (subtraction, multiplication, etc.).
- Graphical user interface.
- Floating-point precision guarantees beyond Python's default behavior.
- Packaging/distribution to package indexes.

## Background
A minimal starting project to practice specification-driven development. Scope is intentionally small: a single arithmetic operation exposed through a command-line interface.

## Requirements

### Functional Requirements
- The tool shall accept two numeric operands (integers or decimals).
- The tool shall support input via command-line arguments (e.g., `python calc.py 2 3`).
- The tool shall support interactive input when no arguments are provided (prompt for each operand).
- The tool shall print the sum of the two operands to standard output.
- The tool shall format whole-number results without a trailing `.0` (e.g., `2.0 + 3.0` prints `5`), using `float.is_integer()` to detect whole values; non-whole decimals retain their fractional part.
- The tool shall support `--help` and `-h` flags to display usage instructions and exit with status code 0.
- The tool shall exit with status code 0 on success.
- The tool shall print an error message to standard error and exit with a non-zero status code when input is not a valid number or when the wrong number of arguments is supplied.

### Non-Functional Requirements
- Compatible with Python 3.8+.
- No third-party dependencies (standard library only).
- Error messages shall be human-readable and include the invalid input.
- Single-file implementation preferred for simplicity.

## Technical Design
A single Python script (e.g., `calc.py`) that:
1. Uses Python's standard `argparse` module to define the CLI, providing automatic `--help` / `-h` flag handling and usage messages on bad arguments.
2. Accepts two positional operands; if no arguments are provided, prompts interactively for each operand.
3. Parses each operand as a number (integer or float).
4. Computes the sum and formats the result using `float.is_integer()` to trim trailing `.0` for whole values, printing the formatted result to standard output.

## Testing Strategy
- Unit tests for the addition logic, input parsing (valid integers, valid floats, invalid strings, missing/extra arguments), and result formatting (whole results print without `.0`, fractional results retain decimals).
- CLI-level tests covering: argument mode, interactive mode, `--help` / `-h` display, and error cases (non-numeric input, wrong argument count).
- Verify exit codes and that errors go to stderr while results go to stdout.

## Decisions
- Whole-number results are formatted without a trailing `.0` (e.g., `2.0 + 3.0` prints `5`) using `float.is_integer()`.
- `--help` / `-h` flags are supported for usage instructions via Python's standard `argparse` module.

## References
- Source draft: this file (originally `specbuddy-type: draft`)
