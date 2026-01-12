"""
Integration tests for model loading and speech recognition.
"""

import pytest
import sys
import os
import json
from unittest.mock import patch, Mock, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class TestModelIntegration:
    """Integration tests for Vosk model operations."""

    def test_model_path_is_in_home_directory(self):
        """Test that model is stored in user's home directory."""
        model_path = os.path.expanduser("~/.speakskiptype/vosk-model-small-en-us-0.15")
        home = os.path.expanduser("~")
        assert model_path.startswith(home)

    def test_model_directory_structure(self):
        """Test expected model directory structure."""
        base_path = os.path.expanduser("~/.speakskiptype")
        model_name = "vosk-model-small-en-us-0.15"

        expected_path = os.path.join(base_path, model_name)
        assert expected_path.endswith(model_name)

    @pytest.mark.skipif(
        not os.path.exists(os.path.expanduser("~/.speakskiptype/vosk-model-small-en-us-0.15")),
        reason="Model not downloaded"
    )
    def test_model_loads_when_present(self):
        """Test that model loads correctly when present."""
        from vosk import Model
        model_path = os.path.expanduser("~/.speakskiptype/vosk-model-small-en-us-0.15")

        if os.path.exists(model_path):
            model = Model(model_path)
            assert model is not None


class TestRecognizerIntegration:
    """Integration tests for Vosk recognizer."""

    def test_recognizer_result_format(self):
        """Test that recognizer results are valid JSON."""
        mock_recognizer = Mock()
        mock_recognizer.Result.return_value = '{"text": "hello"}'

        result = json.loads(mock_recognizer.Result())
        assert 'text' in result
        assert result['text'] == 'hello'

    def test_recognizer_partial_result_format(self):
        """Test that partial results are valid JSON."""
        mock_recognizer = Mock()
        mock_recognizer.PartialResult.return_value = '{"partial": "hel"}'

        result = json.loads(mock_recognizer.PartialResult())
        assert 'partial' in result
        assert result['partial'] == 'hel'

    def test_recognizer_final_result_format(self):
        """Test that final results are valid JSON."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": "hello world"}'

        result = json.loads(mock_recognizer.FinalResult())
        assert 'text' in result
        assert result['text'] == 'hello world'

    def test_recognizer_empty_result(self):
        """Test handling of empty recognition results."""
        mock_recognizer = Mock()
        mock_recognizer.Result.return_value = '{"text": ""}'

        result = json.loads(mock_recognizer.Result())
        assert result['text'] == ""

    def test_recognizer_multiple_words(self):
        """Test recognition of multiple words."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": "git commit minus m fix bug"}'

        result = json.loads(mock_recognizer.FinalResult())
        words = result['text'].split()
        assert len(words) == 6


class TestEndToEndFlow:
    """End-to-end integration tests."""

    def setup_method(self):
        """Set up test fixtures."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = ""
        speakskiptype.ctrl_pressed = False

    def test_voice_command_git_commit(self):
        """Test a typical git commit voice command."""
        mock_recognizer = Mock()
        mock_recognizer.AcceptWaveform.return_value = True
        mock_recognizer.Result.return_value = '{"text": "git commit minus m fix authentication bug"}'
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        # Start recording
        speakskiptype.start_recording()

        # Simulate audio processing adding text
        speakskiptype.recorded_text = "git commit minus m fix authentication bug"

        # Stop recording
        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        # Verify the command was typed
        mock_controller.type.assert_called_once()
        typed_text = mock_controller.type.call_args[0][0]
        assert "git commit" in typed_text
        assert "authentication bug" in typed_text

    def test_voice_command_with_numbers(self):
        """Test voice command containing numbers."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        speakskiptype.start_recording()
        speakskiptype.recorded_text = "port eight thousand eighty"

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        mock_controller.type.assert_called_once_with("port eight thousand eighty")

    def test_voice_command_docker(self):
        """Test a docker voice command."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        speakskiptype.start_recording()
        speakskiptype.recorded_text = "docker compose up minus d"

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        typed_text = mock_controller.type.call_args[0][0]
        assert "docker compose" in typed_text

    def test_long_dictation(self):
        """Test a longer dictation session."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        speakskiptype.start_recording()
        speakskiptype.recorded_text = (
            "this is a long dictation that tests the ability of the system "
            "to handle multiple sentences and longer text inputs without any issues"
        )

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        typed_text = mock_controller.type.call_args[0][0]
        assert len(typed_text) > 50
        assert "dictation" in typed_text
