"""
Unit tests for the Colors class.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from speakskiptype import Colors


class TestColors:
    """Test suite for ANSI color codes."""

    def test_red_color_code(self):
        """Test RED color code is correct ANSI escape sequence."""
        assert Colors.RED == '\033[91m'

    def test_green_color_code(self):
        """Test GREEN color code is correct ANSI escape sequence."""
        assert Colors.GREEN == '\033[92m'

    def test_yellow_color_code(self):
        """Test YELLOW color code is correct ANSI escape sequence."""
        assert Colors.YELLOW == '\033[93m'

    def test_blue_color_code(self):
        """Test BLUE color code is correct ANSI escape sequence."""
        assert Colors.BLUE == '\033[94m'

    def test_magenta_color_code(self):
        """Test MAGENTA color code is correct ANSI escape sequence."""
        assert Colors.MAGENTA == '\033[95m'

    def test_cyan_color_code(self):
        """Test CYAN color code is correct ANSI escape sequence."""
        assert Colors.CYAN == '\033[96m'

    def test_white_color_code(self):
        """Test WHITE color code is correct ANSI escape sequence."""
        assert Colors.WHITE == '\033[97m'

    def test_bold_code(self):
        """Test BOLD code is correct ANSI escape sequence."""
        assert Colors.BOLD == '\033[1m'

    def test_end_code(self):
        """Test END code is correct ANSI escape sequence."""
        assert Colors.END == '\033[0m'

    def test_color_formatting(self):
        """Test that colors can be used in string formatting."""
        formatted = f"{Colors.RED}test{Colors.END}"
        assert formatted == '\033[91mtest\033[0m'

    def test_nested_formatting(self):
        """Test that bold and color can be combined."""
        formatted = f"{Colors.BOLD}{Colors.GREEN}bold green{Colors.END}"
        assert '\033[1m' in formatted
        assert '\033[92m' in formatted
        assert '\033[0m' in formatted
