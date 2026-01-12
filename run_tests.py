#!/usr/bin/env python3
"""
Test runner for SpeakSkipType.
Runs all unit and integration tests with detailed output.
"""

import subprocess
import sys
import os

# Change to project directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
END = '\033[0m'


def print_header(text):
    """Print a formatted header."""
    print(f"\n{BOLD}{CYAN}{'='*60}{END}")
    print(f"{BOLD}{CYAN}{text.center(60)}{END}")
    print(f"{BOLD}{CYAN}{'='*60}{END}\n")


def run_tests(test_type=None, verbose=True):
    """Run pytest with optional filtering."""
    cmd = [sys.executable, '-m', 'pytest']

    if verbose:
        cmd.append('-v')

    cmd.append('--tb=short')

    if test_type == 'unit':
        cmd.extend(['-k', 'unit'])
    elif test_type == 'integration':
        cmd.extend(['-k', 'integration'])

    cmd.append('tests/')

    return subprocess.run(cmd)


def main():
    """Main test runner."""
    print_header("SpeakSkipType Test Suite")

    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print(f"{RED}[!] pytest not installed. Installing...{END}")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pytest', '-q'])
        import pytest

    # Check if numpy is installed (needed for some tests)
    try:
        import numpy
    except ImportError:
        print(f"{YELLOW}[*] Installing numpy for tests...{END}")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'numpy', '-q'])

    # Run all tests
    print(f"{CYAN}Running all tests...{END}\n")
    result = run_tests()

    # Summary
    print_header("Test Summary")

    if result.returncode == 0:
        print(f"{GREEN}{BOLD}All tests passed!{END}")
    else:
        print(f"{RED}{BOLD}Some tests failed. See output above.{END}")

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
