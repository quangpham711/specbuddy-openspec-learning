"""Unit and CLI-level tests for ``calc.py`` using only stdlib ``unittest``.

No third-party test framework is required — all assertions use
``unittest`` which is part of the Python standard library, satisfying
the spec's "No third-party dependencies (standard library only)" rule.
"""

import subprocess
import sys
import unittest
from unittest.mock import patch

from calc import format_result, parse_operand, main


class FormatResultTests(unittest.TestCase):
    """Verify ``format_result`` trims trailing ``.0`` for whole numbers."""

    def test_whole_number_formatting(self):
        self.assertEqual(format_result(5.0), "5")
        self.assertEqual(format_result(0.0), "0")
        self.assertEqual(format_result(-3.0), "-3")

    def test_fractional_formatting(self):
        self.assertEqual(format_result(5.5), "5.5")
        self.assertEqual(format_result(2.25), "2.25")
        self.assertEqual(format_result(-1.5), "-1.5")

    def test_mixed_integer_float(self):
        # int passed to float still formats whole
        self.assertEqual(format_result(7.0), "7")


class ParseOperandTests(unittest.TestCase):
    """Verify ``parse_operand`` accepts valid numbers and rejects junk."""

    def test_valid_integer(self):
        self.assertEqual(parse_operand("42"), 42.0)

    def test_valid_float(self):
        self.assertEqual(parse_operand("3.14"), 3.14)

    def test_valid_scientific_notation(self):
        self.assertEqual(parse_operand("1e2"), 100.0)

    def test_invalid_string_raises(self):
        with self.assertRaises(ValueError):
            parse_operand("notanumber")

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            parse_operand("")


class MainFunctionTests(unittest.TestCase):
    """Test the ``main`` entry-point directly (no subprocess needed)."""

    def test_two_arguments_success(self):
        """``python calc.py 2 3`` → prints ``5``, exits 0."""
        from io import StringIO

        with patch("sys.argv", ["calc.py", "2", "3"]):
            with patch("sys.stdout", new=StringIO()) as out:
                with patch("sys.stderr", new=StringIO()) as err:
                    exit_code = main()
                    self.assertEqual(exit_code, 0)
                    self.assertEqual(out.getvalue().strip(), "5")

    def test_two_arguments_float_success(self):
        """``python calc.py 2.5 3`` → prints ``5.5``, exits 0."""
        from io import StringIO

        with patch("sys.argv", ["calc.py", "2.5", "3"]):
            with patch("sys.stdout", new=StringIO()) as out:
                with patch("sys.stderr", new=StringIO()) as err:
                    exit_code = main()
                    self.assertEqual(exit_code, 0)
                    self.assertEqual(out.getvalue().strip(), "5.5")

    def test_one_argument_prompts_for_second(self):
        """One arg → prompt for second; feeding input via stdin."""
        from io import StringIO

        # Feed the second number; prompt goes to stderr, result to stdout.
        with patch("sys.argv", ["calc.py", "1.5"]):
            with patch("sys.stdin", new=StringIO("2.5")):
                with patch("sys.stderr", new=StringIO()) as err_out:
                    with patch("sys.stdout", new=StringIO()) as out:
                        exit_code = main()
                        self.assertEqual(exit_code, 0)
                        # Prompt text goes to stderr; result goes to stdout.
                        self.assertEqual(out.getvalue().strip(), "4")

    def test_invalid_first_arg_error_stderr(self):
        """Non-numeric first arg → error on stderr, exit 1."""
        with patch("sys.argv", ["calc.py", "abc"]):
            exit_code = main()
            self.assertEqual(exit_code, 1)

    def test_invalid_second_arg_error_stderr(self):
        """Valid first, invalid second → error on stderr, exit 1."""
        from io import StringIO

        with patch("sys.argv", ["calc.py", "5"]):
            with patch("sys.stdin", new=StringIO("notanumber")):
                exit_code = main()
                self.assertEqual(exit_code, 1)


class CLITests(unittest.TestCase):
    """Run ``calc.py`` as an actual subprocess and check stdout/stderr."""

    def _run_calc(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "calc.py", *args],
            capture_output=True,
            text=True,
            timeout=10,
        )

    def test_cli_two_args(self):
        """``python calc.py 2 3`` → stdout ``5``, exit 0."""
        proc = self._run_calc("2", "3")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "5")
        self.assertEqual(proc.stderr.strip(), "")

    def test_cli_help(self):
        """``python calc.py --help`` exits 0 and shows usage."""
        proc = self._run_calc("--help")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("usage", (proc.stdout + proc.stderr).lower())

    def test_cli_help_short(self):
        """``python calc.py -h`` exits 0 and shows usage."""
        proc = self._run_calc("-h")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("usage", (proc.stdout + proc.stderr).lower())

    def test_cli_invalid_input(self):
        """``python calc.py abc 1`` → stderr error, exit non-zero."""
        proc = self._run_calc("abc", "1")
        self.assertNotEqual(proc.returncode, 0)
        self.assertTrue(proc.stderr.strip() != "")

    def test_cli_wrong_arg_count(self):
        """Too many args → argparse error, exit non-zero."""
        proc = self._run_calc("1", "2", "3")
        self.assertNotEqual(proc.returncode, 0)

    def test_cli_subtract_long_flag(self):
        """``python calc.py 5 3 --subtract`` → stdout ``2``, exit 0."""
        proc = self._run_calc("5", "3", "--subtract")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "2")
        self.assertEqual(proc.stderr.strip(), "")

    def test_cli_subtract_short_flag_before_operands(self):
        """``python calc.py -s 5 3`` → stdout ``2``, exit 0."""
        proc = self._run_calc("-s", "5", "3")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "2")

    def test_cli_subtract_negative_result(self):
        """``python calc.py 5 7 -s`` → stdout ``-2``, exit 0."""
        proc = self._run_calc("5", "7", "-s")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "-2")

    def test_cli_subtract_fractional_result(self):
        """``python calc.py 2.25 3 --subtract`` → stdout ``-0.75``, exit 0."""
        proc = self._run_calc("2.25", "3", "--subtract")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "-0.75")

    def test_cli_help_mentions_subtraction(self):
        """``python calc.py --help`` shows the ``--subtract`` flag."""
        proc = self._run_calc("--help")
        self.assertEqual(proc.returncode, 0)
        output = proc.stdout + proc.stderr
        self.assertIn("--subtract", output)
        self.assertIn("-s", output)