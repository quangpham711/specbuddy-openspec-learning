# Mini Calculator Specification

## Purpose

A single-file Python CLI calculator that adds or subtracts two numbers, accepting input via command-line arguments or interactive prompts and formatting whole-number results cleanly.

## Requirements

### Requirement: Two-operand addition
The tool SHALL add two numeric operands (integers or decimals) when no operation flag is given and SHALL print their sum to standard output.

#### Scenario: Add via command-line arguments
- **WHEN** a user runs `calc.py 2 3`
- **THEN** the tool prints `5` to standard output and exits with status code 0

#### Scenario: Add decimal operands
- **WHEN** a user runs `calc.py 2.5 3`
- **THEN** the tool prints `5.5` to standard output and exits with status code 0

### Requirement: Subtraction via flag
The tool SHALL subtract the second operand from the first when the user passes `--subtract` or its short form `-s`, and SHALL print the difference to standard output.

#### Scenario: Subtract with long flag
- **WHEN** a user runs `calc.py 5 3 --subtract`
- **THEN** the tool prints `2` to standard output and exits with status code 0

#### Scenario: Subtract with short flag
- **WHEN** a user runs `calc.py -s 5 3`
- **THEN** the tool prints `2` to standard output and exits with status code 0

#### Scenario: Subtraction producing a negative result
- **WHEN** a user runs `calc.py 5 7 --subtract`
- **THEN** the tool prints `-2` to standard output and exits with status code 0

### Requirement: Backward-compatible default action
The tool SHALL behave identically to the pre-change calculator when no operation flag is supplied: two operands are added.

#### Scenario: No flag defaults to addition
- **WHEN** a user runs `calc.py 2 3` exactly as before the change
- **THEN** the tool prints `5` to standard output and exits with status code 0

### Requirement: Interactive input
The tool SHALL prompt interactively for each operand when fewer than two operands are supplied on the command line. The tool SHALL never prompt for an operation in interactive mode, and SHALL default to addition when no operation flag is given. Prompts SHALL be written to standard error so standard output remains clean for the result.

#### Scenario: No arguments prompts for both operands
- **WHEN** a user runs `calc.py` with no operands and enters `2` then `3` at the prompts
- **THEN** the tool prints `5` to standard output and exits with status code 0

#### Scenario: One argument prompts for the second operand
- **WHEN** a user runs `calc.py 1.5` and enters `2.5` at the prompt
- **THEN** the tool prints `4` to standard output and exits with status code 0

### Requirement: Whole-number result formatting
The tool SHALL format whole-number results without a trailing `.0` (for example `2.0 3.0` prints `5`) and SHALL retain the fractional part of non-whole results.

#### Scenario: Whole-number operands produce trimmed output
- **WHEN** a user runs `calc.py 2.0 3.0`
- **THEN** the tool prints `5` (not `5.0`) to standard output and exits with status code 0

#### Scenario: Fractional results keep their decimals
- **WHEN** a user runs `calc.py 2.25 3 --subtract`
- **THEN** the tool prints `-0.75` to standard output and exits with status code 0

### Requirement: Help flag
The tool SHALL support `--help` and `-h` flags to display usage instructions describing both operations and SHALL exit with status code 0 when they are used.

#### Scenario: Help via long flag
- **WHEN** a user runs `calc.py --help`
- **THEN** the tool displays usage text that includes subtraction and exits with status code 0

#### Scenario: Help via short flag
- **WHEN** a user runs `calc.py -h`
- **THEN** the tool displays usage text and exits with status code 0

### Requirement: Error handling and exit codes
The tool SHALL exit with status code 0 on success. It SHALL print a human-readable error message including the invalid input to standard error and exit with a non-zero status code when an operand is not a valid number or when more than two operands are supplied.

#### Scenario: Non-numeric operand is an error
- **WHEN** a user runs `calc.py abc 1`
- **THEN** the tool prints an error message containing the invalid input `abc` to standard error and exits with a non-zero status code

#### Scenario: Too many operands is an error
- **WHEN** a user runs `calc.py 1 2 3`
- **THEN** the tool prints an error message to standard error and exits with a non-zero status code

#### Scenario: Successful run exits zero
- **WHEN** a user runs `calc.py 8 3 --subtract`
- **THEN** the tool prints `5` to standard output and exits with status code 0