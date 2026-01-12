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
    shift_l = Mock()
    shift_r = Mock()
    ctrl = Mock()


class TestCtrlPressedState:
    """Test suite for ctrl_pressed state management."""

    def setup_method(self):
        """Set up the mock Key before each test."""
        speakskiptype.Key = MockKey
        speakskiptype.ctrl_pressed = False
        speakskiptype.shift_pressed = False
        speakskiptype.hold_to_record_active = False

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

    def test_shift_press_sets_flag(self):
        """Test that pressing Shift sets shift_pressed."""
        speakskiptype.shift_pressed = False
        speakskiptype.on_press(MockKey.shift_l)
        assert speakskiptype.shift_pressed is True

    def test_shift_release_clears_flag(self):
        """Test that releasing Shift clears shift_pressed."""
        speakskiptype.shift_pressed = True
        speakskiptype.on_release(MockKey.shift_l)
        assert speakskiptype.shift_pressed is False


class TestHotkeyHandling:
    """Test suite for hotkey combinations."""

    def setup_method(self):
        """Set up the mock Key before each test."""
        speakskiptype.Key = MockKey
        speakskiptype.ctrl_pressed = False
        speakskiptype.shift_pressed = False
        speakskiptype.is_recording = False
        speakskiptype.hold_to_record_active = False

    def test_ctrl_r_starts_recording(self):
        """Test that Ctrl+R starts recording when not recording."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = False
        speakskiptype.shift_pressed = False

        mock_key = Mock()
        mock_key.char = 'r'

        with patch.object(speakskiptype, 'play_beep'):
            speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is True

    def test_ctrl_r_raw_code_starts_recording(self):
        """Test that Ctrl+R with raw code starts recording."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = False
        speakskiptype.shift_pressed = False

        mock_key = Mock()
        mock_key.char = '\x12'  # Raw Ctrl+R code

        with patch.object(speakskiptype, 'play_beep'):
            speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is True

    def test_ctrl_r_toggles_recording(self):
        """Test that Ctrl+R toggles recording (new behavior)."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = True
        speakskiptype.shift_pressed = False
        speakskiptype.recorded_text = "test"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()
        speakskiptype.config = {'output': {'add_space_after': False, 'method': 'clipboard'}}

        mock_key = Mock()
        mock_key.char = 'r'

        with patch.object(speakskiptype, 'play_beep'):
            with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True):
                with patch.object(speakskiptype, 'paste_from_clipboard'):
                    with patch.object(speakskiptype, 'add_to_history'):
                        with patch('time.sleep'):
                            speakskiptype.on_press(mock_key)

        # Should have stopped (toggled)
        assert speakskiptype.is_recording is False

    def test_ctrl_s_stops_recording(self):
        """Test that Ctrl+S stops recording and types."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "test"
        speakskiptype.shift_pressed = False
        speakskiptype.config = {'output': {'add_space_after': False, 'method': 'clipboard'}}

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        mock_key = Mock()
        mock_key.char = 's'

        with patch.object(speakskiptype, 'play_beep'):
            with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True):
                with patch.object(speakskiptype, 'paste_from_clipboard'):
                    with patch.object(speakskiptype, 'add_to_history'):
                        with patch('time.sleep'):
                            speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is False

    def test_ctrl_s_raw_code_stops_recording(self):
        """Test that Ctrl+S with raw code stops recording."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""
        speakskiptype.shift_pressed = False
        speakskiptype.config = {'output': {'add_space_after': False, 'method': 'clipboard'}}

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()

        mock_key = Mock()
        mock_key.char = '\x13'  # Raw Ctrl+S code

        with patch.object(speakskiptype, 'play_beep'):
            with patch('time.sleep'):
                speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is False

    def test_r_without_ctrl_does_nothing(self):
        """Test that pressing R without Ctrl doesn't start recording."""
        speakskiptype.ctrl_pressed = False
        speakskiptype.is_recording = False

        mock_key = Mock()
        mock_key.char = 'r'

        speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is False

    def test_s_without_ctrl_does_nothing(self):
        """Test that pressing S without Ctrl doesn't stop recording."""
        speakskiptype.ctrl_pressed = False
        speakskiptype.is_recording = True

        mock_key = Mock()
        mock_key.char = 's'

        speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is True

    def test_other_key_with_ctrl(self):
        """Test that other keys with Ctrl don't affect recording."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = False

        mock_key = Mock()
        mock_key.char = 'a'

        speakskiptype.on_press(mock_key)

        assert speakskiptype.is_recording is False

    def test_special_key_handling(self):
        """Test that special keys without char attribute are handled."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.is_recording = False

        mock_key = Mock(spec=[])  # No char attribute

        # Should not raise
        speakskiptype.on_press(mock_key)
        assert speakskiptype.is_recording is False


class TestHoldToRecord:
    """Test suite for hold-to-record functionality."""

    def setup_method(self):
        """Set up before each test."""
        speakskiptype.Key = MockKey
        speakskiptype.ctrl_pressed = False
        speakskiptype.shift_pressed = False
        speakskiptype.is_recording = False
        speakskiptype.hold_to_record_active = False

    def test_ctrl_shift_r_starts_hold_to_record(self):
        """Test that Ctrl+Shift+R activates hold-to-record mode."""
        speakskiptype.ctrl_pressed = True
        speakskiptype.shift_pressed = True
        speakskiptype.is_recording = False

        mock_key = Mock()
        mock_key.char = 'r'

        with patch.object(speakskiptype, 'play_beep'):
            speakskiptype.on_press(mock_key)

        assert speakskiptype.hold_to_record_active is True
        assert speakskiptype.is_recording is True

    def test_release_ctrl_stops_hold_to_record(self):
        """Test that releasing Ctrl stops hold-to-record and types."""
        speakskiptype.hold_to_record_active = True
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "test"
        speakskiptype.config = {'output': {'add_space_after': False, 'method': 'clipboard'}}

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()

        with patch.object(speakskiptype, 'play_beep'):
            with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True):
                with patch.object(speakskiptype, 'paste_from_clipboard'):
                    with patch.object(speakskiptype, 'add_to_history'):
                        with patch('time.sleep'):
                            speakskiptype.on_release(MockKey.ctrl_l)

        assert speakskiptype.hold_to_record_active is False
        assert speakskiptype.is_recording is False
