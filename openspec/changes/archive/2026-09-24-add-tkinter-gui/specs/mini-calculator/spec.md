# Spec Delta

## ADDED Requirements

### Requirement: GUI mode for the calculator
The tool SHALL open a simple desktop GUI when invoked with the `--gui` flag. The GUI SHALL provide two numeric input fields, an operation selection for Add or Subtract, a Compute button, and a result display. The tool SHALL compute results in the GUI using the same operand parsing and result formatting as the CLI, SHALL display a human-readable inline error message that includes the invalid input when an operand is not a valid number, and SHALL keep the window open after each computation.

#### Scenario: GUI opens via the --gui flag
- **WHEN** a user runs `calc.py --gui`
- **THEN** a window opens with two number input fields, an Add/Subtract operation selection, a Compute button, and a result display showing no result yet

#### Scenario: Compute in the GUI shows a formatted sum
- **WHEN** a user enters `2` and `3`, selects Add, and clicks Compute
- **THEN** the result display shows `5`

#### Scenario: Compute in the GUI shows a formatted difference
- **WHEN** a user enters `5` and `3`, selects Subtract, and clicks Compute
- **THEN** the result display shows `2`

#### Scenario: Whole-number GUI results are trimmed
- **WHEN** a user enters `2.0` and `3.0`, selects Add, and clicks Compute
- **THEN** the result display shows `5` and not `5.0`

#### Scenario: Non-numeric input shows an inline error
- **WHEN** a user enters `abc` and `3` and clicks Compute
- **THEN** the GUI shows an inline error message containing `abc` and the result display shows no result

#### Scenario: CLI behavior is preserved without --gui
- **WHEN** a user runs `calc.py` without the `--gui` flag
- **THEN** the tool behaves exactly as before, including interactive prompting for missing operands, stderr prompts, and exit codes

#### Scenario: Help lists the --gui flag
- **WHEN** a user runs `calc.py --help`
- **THEN** the usage text describes the `--gui` flag

#### Scenario: GUI launch fails gracefully without Tk
- **WHEN** a user runs `calc.py --gui` on a Python build without Tk installed
- **THEN** the tool prints a clear error message and exits with a non-zero status code, and the CLI remains usable without the `--gui` flag