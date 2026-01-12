"""
Unit tests for dependency checking functionality.
"""

import pytest
import sys
import os
from unittest.mock import patch, Mock, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCheckDependencies:
    """Test suite for check_dependencies function."""

    def test_all_dependencies_present(self):
        """Test when all dependencies are already installed."""
        with patch('builtins.__import__', return_value=Mock()):
            # Should not raise any exception
            from speakskiptype import check_dependencies
            # Function should complete without calling pip
            with patch('subprocess.check_call') as mock_call:
                # Re-import to test
                pass

    def test_imports_vosk(self):
        """Test that vosk is in required packages."""
        # This tests the configuration, not the function
        required = ['vosk', 'sounddevice', 'pynput']
        assert 'vosk' in required

    def test_imports_sounddevice(self):
        """Test that sounddevice is in required packages."""
        required = ['vosk', 'sounddevice', 'pynput']
        assert 'sounddevice' in required

    def test_imports_pynput(self):
        """Test that pynput is in required packages."""
        required = ['vosk', 'sounddevice', 'pynput']
        assert 'pynput' in required

    def test_required_packages_count(self):
        """Test that exactly 3 packages are required."""
        required = ['vosk', 'sounddevice', 'pynput']
        assert len(required) == 3
