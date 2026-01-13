"""
Unit tests for recording functionality.
"""

import pytest
import sys
import os
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class TestStartRecording:
    """Test suite for start_recording function."""

    def setup_method(self):
        """Reset state before each test."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = ""

    def test_start_recording_sets_flag(self):
        """Test that start_recording sets is_recording to True."""
        speakskiptype.is_recording = False
        
        with patch.object(speakskiptype, 'play_beep'):
            speakskiptype.start_recording()
        
        assert speakskiptype.is_recording is True

    def test_start_recording_clears_text(self):
        """Test that start_recording clears recorded_text."""
        speakskiptype.recorded_text = "old text"
        speakskiptype.is_recording = False
        
        with patch.object(speakskiptype, 'play_beep'):
            speakskiptype.start_recording()
        
        assert speakskiptype.recorded_text == ""

    def test_start_recording_idempotent(self):
        """Test that calling start when already recording toggles to stop."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "some text"
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
                            speakskiptype.start_recording()
        
        # Toggle behavior: should stop recording
        assert speakskiptype.is_recording is False

    def test_start_recording_when_already_recording(self):
        """Test toggle behavior when already recording."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "existing text"
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
                            speakskiptype.start_recording()
        
        # Should have stopped (toggle)
        assert speakskiptype.is_recording is False


class TestStopRecording:
    """Test suite for stop_recording_and_type function."""

    def setup_method(self):
        """Reset state before each test."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = ""
        speakskiptype.config = {'output': {'add_space_after': False, 'method': 'clipboard'},
                                'voice_commands': {'enabled': False}}

    def test_stop_recording_not_recording(self):
        """Test that stop does nothing when not recording."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = "should not change"
        
        speakskiptype.stop_recording_and_type()
        
        assert speakskiptype.recorded_text == "should not change"

    def test_stop_recording_sets_flag_false(self):
        """Test that stop_recording sets is_recording to False."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""
        
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()
        
        with patch.object(speakskiptype, 'play_beep'):
            with patch('time.sleep'):
                speakskiptype.stop_recording_and_type()
        
        assert speakskiptype.is_recording is False

    def test_stop_recording_types_text(self):
        """Test that stop_recording types the recorded text."""
        import copy
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "hello world"
        # Ensure config is properly set up
        speakskiptype.config = copy.deepcopy(speakskiptype.DEFAULT_CONFIG)
        speakskiptype.config['transcription']['auto_punctuation'] = False
        speakskiptype.config['output']['add_space_after'] = False

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch.object(speakskiptype, 'play_beep'):
            with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True) as mock_copy:
                with patch.object(speakskiptype, 'paste_from_clipboard'):
                    with patch.object(speakskiptype, 'add_to_history'):
                        with patch.object(speakskiptype, 'update_stats'):
                            with patch('time.sleep'):
                                speakskiptype.stop_recording_and_type()

        mock_copy.assert_called_once_with("hello world")

    def test_stop_recording_appends_final_text(self):
        """Test that final recognition result is appended."""
        import copy
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "hello "
        # Ensure config is properly set up
        speakskiptype.config = copy.deepcopy(speakskiptype.DEFAULT_CONFIG)
        speakskiptype.config['transcription']['auto_punctuation'] = False
        speakskiptype.config['output']['add_space_after'] = False

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": "world"}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch.object(speakskiptype, 'play_beep'):
            with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True) as mock_copy:
                with patch.object(speakskiptype, 'paste_from_clipboard'):
                    with patch.object(speakskiptype, 'add_to_history'):
                        with patch.object(speakskiptype, 'update_stats'):
                            with patch('time.sleep'):
                                speakskiptype.stop_recording_and_type()

        # Should have combined text
        call_arg = mock_copy.call_args[0][0]
        assert "hello" in call_arg
        assert "world" in call_arg

    def test_stop_recording_no_text_detected(self, capsys):
        """Test message when no speech is detected."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""
        speakskiptype.background_mode = False
        
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()
        
        with patch.object(speakskiptype, 'play_beep'):
            with patch('time.sleep'):
                speakskiptype.stop_recording_and_type()
        
        captured = capsys.readouterr()
        assert "No speech detected" in captured.out or "No speech" in captured.out
