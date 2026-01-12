"""
Unit tests for display/printing functionality.
"""

import pytest
import sys
import os
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype
from speakskiptype import Colors


class TestPrintBanner:
    """Test suite for print_banner function."""

    def test_print_banner_contains_name(self, capsys):
        """Test that banner contains SpeakSkipType name."""
        speakskiptype.print_banner()
        captured = capsys.readouterr()
        # Check for ASCII art characters that spell "Speak"
        assert "Speak" in captured.out or "___" in captured.out

    def test_print_banner_contains_colors(self, capsys):
        """Test that banner contains color codes."""
        speakskiptype.print_banner()
        captured = capsys.readouterr()
        assert '\033[' in captured.out  # ANSI escape sequence

    def test_print_banner_contains_tagline(self, capsys):
        """Test that banner contains the tagline."""
        speakskiptype.print_banner()
        captured = capsys.readouterr()
        assert "FREE" in captured.out or "terminal" in captured.out.lower()


class TestPrintControls:
    """Test suite for print_controls function."""

    def test_print_controls_shows_ctrl_r(self, capsys):
        """Test that controls show Ctrl+R."""
        speakskiptype.print_controls()
        captured = capsys.readouterr()
        assert "Ctrl" in captured.out
        assert "R" in captured.out

    def test_print_controls_shows_ctrl_s(self, capsys):
        """Test that controls show Ctrl+S."""
        speakskiptype.print_controls()
        captured = capsys.readouterr()
        assert "Ctrl" in captured.out
        assert "S" in captured.out

    def test_print_controls_shows_ctrl_q(self, capsys):
        """Test that controls show Ctrl+Q."""
        speakskiptype.print_controls()
        captured = capsys.readouterr()
        assert "Ctrl" in captured.out
        assert "Q" in captured.out

    def test_print_controls_shows_recording_hint(self, capsys):
        """Test that controls show recording action hint."""
        speakskiptype.print_controls()
        captured = capsys.readouterr()
        assert "Recording" in captured.out or "recording" in captured.out

    def test_print_controls_shows_stop_hint(self, capsys):
        """Test that controls show stop action hint."""
        speakskiptype.print_controls()
        captured = capsys.readouterr()
        assert "Stop" in captured.out or "Type" in captured.out

    def test_print_controls_shows_quit_hint(self, capsys):
        """Test that controls show quit action hint."""
        speakskiptype.print_controls()
        captured = capsys.readouterr()
        assert "Quit" in captured.out or "Exit" in captured.out

    def test_print_controls_has_formatting(self, capsys):
        """Test that controls have color formatting."""
        speakskiptype.print_controls()
        captured = capsys.readouterr()
        assert '\033[' in captured.out  # ANSI escape sequence
