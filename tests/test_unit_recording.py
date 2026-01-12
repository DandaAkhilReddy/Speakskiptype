"""
Unit tests for recording functionality.
"""

import pytest
import sys
import os
from unittest.mock import patch, Mock, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class TestStartRecording:
    """Test suite for start_recording function."""

    def test_start_recording_sets_flag(self):
        """Test that start_recording sets is_recording to True."""
        speakskiptype.is_recording = False
        speakskiptype.start_recording()
        assert speakskiptype.is_recording is True

    def test_start_recording_clears_text(self):
        """Test that start_recording clears recorded_text."""
        speakskiptype.recorded_text = "previous text"
        speakskiptype.is_recording = False
        speakskiptype.start_recording()
        assert speakskiptype.recorded_text == ""

    def test_start_recording_idempotent(self):
        """Test that calling start_recording twice doesn't change state."""
        speakskiptype.is_recording = False
        speakskiptype.start_recording()
        speakskiptype.recorded_text = "some text"
        # Calling again should not clear text since already recording
        speakskiptype.start_recording()
        assert speakskiptype.recorded_text == "some text"

    def test_start_recording_when_already_recording(self):
        """Test that start_recording does nothing when already recording."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "existing text"
        speakskiptype.start_recording()
        # Text should NOT be cleared
        assert speakskiptype.recorded_text == "existing text"


class TestStopRecording:
    """Test suite for stop_recording_and_type function."""

    def test_stop_recording_not_recording(self):
        """Test that stop_recording does nothing when not recording."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = ""
        # Should not raise any exception
        with patch.object(speakskiptype, 'recognizer') as mock_rec:
            mock_rec.FinalResult.return_value = '{"text": ""}'
            # This should return early
            speakskiptype.stop_recording_and_type()
        assert speakskiptype.is_recording is False

    def test_stop_recording_sets_flag_false(self):
        """Test that stop_recording sets is_recording to False."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "test"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        assert speakskiptype.is_recording is False

    def test_stop_recording_types_text(self):
        """Test that stop_recording types the recorded text."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "hello world"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        mock_controller.type.assert_called_once_with("hello world")

    def test_stop_recording_appends_final_text(self):
        """Test that stop_recording appends final recognition result."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "hello "

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": "world"}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        # Should type "hello world" (trimmed)
        mock_controller.type.assert_called_once_with("hello world")

    def test_stop_recording_no_text_detected(self):
        """Test behavior when no speech was detected."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        # type should NOT be called when no text
        mock_controller.type.assert_not_called()
