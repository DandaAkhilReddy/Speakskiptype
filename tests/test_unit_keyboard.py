"""
Unit tests for keyboard handling functionality.
"""

import pytest
import sys
import os
from unittest.mock import patch, Mock, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class MockKey:
    """Mock Key class for testing."""
    ctrl_l = Mock()
    ctrl_r = Mock()


class TestCtrlPressedState:
    """Test suite for ctrl_pressed state management."""

    def setup_method(self):
        """Set up the mock Key before each test."""
        speakskiptype.Key = MockKey

    def test_initial_ctrl_state_false(self):
        """Test that ctrl_pressed starts as False."""
        speakskiptype.ctrl_pressed = False
        assert speakskiptype.ctrl_pressed is False

    def test_ctrl_left_press_sets_flag(self):
        """Test that pressing left Ctrl sets ctrl_pressed."""
        speakskiptype.ctrl_pressed = False
        speakskiptype.on_press(MockKey.ctrl_l)
        assert speakskiptype.ctrl_pressed is True

    def test_ctrl_right_press_sets_flag(self):
        """Test that pressing right Ctrl sets ctrl_pressed."""
        speakskiptype.ctrl_pressed = False
        speakskiptype.on_press(MockKey.ctrl_r)
        assert speakskiptype.ctrl_pressed is True

    def test_ctrl_left_release_clears_flag(self):
        """Test that releasing left Ctrl clears ctrl_pressed."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.on_release(MockKey.ctrl_l)
        assert speakskiptype.ctrl_pressed is False

    def test_ctrl_right_release_clears_flag(self):
        """Test that releasing right Ctrl clears ctrl_pressed."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.on_release(MockKey.ctrl_r)
        assert speakskiptype.ctrl_pressed is False

    def test_other_key_release_keeps_flag(self):
        """Test that releasing other keys doesn't affect ctrl_pressed."""
        speakskiptype.ctrl_pressed = True
        mock_key = Mock()
        mock_key.char = 'a'
        speakskiptype.on_release(mock_key)
        assert speakskiptype.ctrl_pressed is True


class TestHotkeyHandling:
    """Test suite for hotkey combinations."""

    def setup_method(self):
        """Set up the mock Key before each test."""
        speakskiptype.Key = MockKey

    def test_ctrl_r_starts_recording(self):
        """Test that Ctrl+R starts recording."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = False

        mock_key = Mock()
        mock_key.char = 'r'

        result = speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is True
        assert result is False  # Don't propagate

    def test_ctrl_r_raw_code_starts_recording(self):
        """Test that Ctrl+R with raw code starts recording."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = False

        mock_key = Mock()
        mock_key.char = '\x12'  # Raw Ctrl+R code

        result = speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is True

    def test_ctrl_s_stops_recording(self):
        """Test that Ctrl+S stops recording and types."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "test"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        mock_key = Mock()
        mock_key.char = 's'

        with patch('time.sleep'):
            result = speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is False
        assert result is False

    def test_ctrl_s_raw_code_stops_recording(self):
        """Test that Ctrl+S with raw code stops recording."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        mock_key = Mock()
        mock_key.char = '\x13'  # Raw Ctrl+S code

        with patch('time.sleep'):
            result = speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is False

    def test_r_without_ctrl_does_nothing(self):
        """Test that R without Ctrl doesn't start recording."""
        speakskiptype.ctrl_pressed = False
        speakskiptype.is_recording = False

        mock_key = Mock()
        mock_key.char = 'r'

        speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is False

    def test_s_without_ctrl_does_nothing(self):
        """Test that S without Ctrl doesn't stop recording."""
        speakskiptype.ctrl_pressed = False
        speakskiptype.is_recording = True

        mock_key = Mock()
        mock_key.char = 's'

        speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is True

    def test_other_key_with_ctrl(self):
        """Test that other keys with Ctrl do nothing."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = False

        mock_key = Mock()
        mock_key.char = 'a'

        speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is False

    def test_special_key_handling(self):
        """Test that special keys (without char) don't cause errors."""
        speakskiptype.ctrl_pressed = True

        # Key without char attribute
        mock_key = Mock(spec=[])

        # Should not raise exception
        speakskiptype.on_press(mock_key)


class TestOnHotkey:
    """Test suite for on_hotkey function."""

    def test_on_hotkey_with_char_returns_none(self):
        """Test that on_hotkey with char attribute returns None."""
        mock_key = Mock()
        mock_key.char = 'r'
        result = speakskiptype.on_hotkey(mock_key)
        assert result is None

    def test_on_hotkey_without_char_returns_none(self):
        """Test that on_hotkey without char attribute returns None."""
        mock_key = Mock(spec=[])
        result = speakskiptype.on_hotkey(mock_key)
        assert result is None
