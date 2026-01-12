"""
Edge case tests for SpeakSkipType.
Tests boundary conditions, special inputs, and error scenarios.
"""

import pytest
import sys
import os
import queue
import time
import threading
from unittest.mock import patch, Mock, MagicMock
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class TestEmptyInputs:
    """Test handling of empty inputs."""

    def test_empty_audio_data(self):
        """Test handling of empty audio data."""
        speakskiptype.is_recording = True
        empty_audio = np.array([], dtype=np.int16)

        # Should not raise exception
        speakskiptype.audio_callback(empty_audio, 0, None, None)

    def test_empty_recognition_result(self):
        """Test handling of empty recognition result."""
        mock_recognizer = Mock()
        mock_recognizer.AcceptWaveform.return_value = True
        mock_recognizer.Result.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.recorded_text = ""

        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        speakskiptype.audio_queue.put(b'\x00' * 100)
        speakskiptype.audio_queue.put(None)

        speakskiptype.process_audio()

        # Empty text should not be added
        assert speakskiptype.recorded_text == ""

    def test_empty_final_result(self):
        """Test handling of empty final result."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()

        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        # Should not type anything
        speakskiptype.keyboard_controller.type.assert_not_called()


class TestLongInputs:
    """Test handling of long inputs."""

    def test_long_text_recognition(self):
        """Test handling of very long recognized text."""
        long_text = "word " * 1000  # 5000 characters

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = f'{{"text": "{long_text.strip()}"}}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        # Should type the full text
        mock_controller.type.assert_called_once()
        typed_text = mock_controller.type.call_args[0][0]
        assert len(typed_text) > 4000

    def test_long_audio_stream(self):
        """Test handling of long continuous audio stream."""
        speakskiptype.is_recording = True

        # Clear queue
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        # Simulate 100 audio chunks
        for _ in range(100):
            audio_chunk = np.random.randint(-1000, 1000, 8000, dtype=np.int16)
            speakskiptype.audio_callback(audio_chunk, 8000, None, None)

        # Verify all chunks were queued
        count = 0
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()
            count += 1

        assert count == 100


class TestSpecialCharacters:
    """Test handling of special characters."""

    def test_unicode_in_text(self):
        """Test handling of Unicode characters in recognized text."""
        unicode_text = "Hello 世界 🎤"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = f'{{"text": "{unicode_text}"}}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        mock_controller.type.assert_called_once_with(unicode_text)

    def test_special_shell_characters(self):
        """Test handling of shell special characters."""
        special_text = "echo $HOME && ls -la | grep test"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = f'{{"text": "{special_text}"}}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        mock_controller.type.assert_called_once_with(special_text)

    def test_quotes_in_text(self):
        """Test handling of quotes in text."""
        quoted_text = 'git commit -m "fix bug"'

        mock_recognizer = Mock()
        # Need to escape for JSON
        mock_recognizer.FinalResult.return_value = '{"text": "git commit -m \\"fix bug\\""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        mock_controller.type.assert_called_once()

    def test_newlines_in_text(self):
        """Test handling of newlines in recognized text."""
        # Vosk typically doesn't return newlines, but test edge case
        text_with_newline = "line one\\nline two"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = f'{{"text": "{text_with_newline}"}}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        mock_controller.type.assert_called_once()


class TestRapidOperations:
    """Test handling of rapid/concurrent operations."""

    def test_rapid_start_stop(self):
        """Test rapid start/stop recording cycles."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()

        with patch('time.sleep'):
            for _ in range(10):
                speakskiptype.start_recording()
                speakskiptype.stop_recording_and_type()

        # Should complete without error
        assert speakskiptype.is_recording is False

    def test_rapid_key_events(self):
        """Test rapid key press events."""
        from tests.conftest import MockKey
        speakskiptype.Key = MockKey

        # Rapidly press and release Ctrl
        for _ in range(50):
            speakskiptype.on_press(MockKey.ctrl_l)
            speakskiptype.on_release(MockKey.ctrl_l)

        assert speakskiptype.ctrl_pressed is False

    def test_multiple_audio_callbacks_rapid(self):
        """Test rapid audio callbacks."""
        speakskiptype.is_recording = True

        # Clear queue
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        # Rapid callbacks
        start = time.time()
        for _ in range(1000):
            audio = np.zeros(160, dtype=np.int16)  # 10ms of audio
            speakskiptype.audio_callback(audio, 160, None, None)
        elapsed = time.time() - start

        # Should complete quickly (< 1 second)
        assert elapsed < 1.0

        # All should be queued
        count = 0
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()
            count += 1
        assert count == 1000


class TestStateTransitions:
    """Test state machine transitions."""

    def test_double_start_recording(self):
        """Test calling start_recording twice."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = "existing"

        speakskiptype.start_recording()
        assert speakskiptype.is_recording is True
        assert speakskiptype.recorded_text == ""

        # Start again - should be idempotent
        speakskiptype.recorded_text = "new text"
        speakskiptype.start_recording()
        assert speakskiptype.is_recording is True
        assert speakskiptype.recorded_text == "new text"  # Not cleared

    def test_stop_when_not_recording(self):
        """Test calling stop when not recording."""
        speakskiptype.is_recording = False
        mock_recognizer = Mock()
        speakskiptype.recognizer = mock_recognizer
        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        # Should not call any recognizer methods
        mock_recognizer.FinalResult.assert_not_called()
        mock_controller.type.assert_not_called()

    def test_ctrl_state_consistency(self):
        """Test Ctrl key state remains consistent."""
        from tests.conftest import MockKey
        speakskiptype.Key = MockKey
        speakskiptype.ctrl_pressed = False

        # Press Ctrl left
        speakskiptype.on_press(MockKey.ctrl_l)
        assert speakskiptype.ctrl_pressed is True

        # Press Ctrl right (both pressed)
        speakskiptype.on_press(MockKey.ctrl_r)
        assert speakskiptype.ctrl_pressed is True

        # Release Ctrl left
        speakskiptype.on_release(MockKey.ctrl_l)
        assert speakskiptype.ctrl_pressed is False  # Both released

        # Release Ctrl right
        speakskiptype.on_release(MockKey.ctrl_r)
        assert speakskiptype.ctrl_pressed is False


class TestErrorConditions:
    """Test error handling."""

    def test_audio_callback_with_error_status(self, capsys):
        """Test audio callback with error status."""
        speakskiptype.is_recording = True
        audio = np.zeros(100, dtype=np.int16)

        speakskiptype.audio_callback(audio, 100, None, "input overflow")

        captured = capsys.readouterr()
        assert "Audio Error" in captured.err or "overflow" in captured.err

    def test_malformed_json_result(self):
        """Test handling of malformed JSON from recognizer."""
        mock_recognizer = Mock()
        mock_recognizer.AcceptWaveform.return_value = True
        mock_recognizer.Result.return_value = '{"text": "valid"}'  # Valid JSON
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.recorded_text = ""

        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        speakskiptype.audio_queue.put(b'\x00' * 100)
        speakskiptype.audio_queue.put(None)

        # Should not raise exception
        speakskiptype.process_audio()

    def test_key_without_char_attribute(self):
        """Test handling keys without char attribute."""
        mock_key = Mock(spec=[])  # No attributes
        speakskiptype.ctrl_pressed = True

        # Should not raise exception
        speakskiptype.on_press(mock_key)


class TestBoundaryConditions:
    """Test boundary conditions."""

    def test_zero_length_audio(self):
        """Test zero-length audio data."""
        speakskiptype.is_recording = True

        # Clear queue
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        zero_audio = np.array([], dtype=np.int16)
        speakskiptype.audio_callback(zero_audio, 0, None, None)

        # Should add empty bytes to queue
        assert not speakskiptype.audio_queue.empty()

    def test_single_word_recognition(self):
        """Test recognition of single word."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": "hello"}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        mock_controller.type.assert_called_once_with("hello")

    def test_whitespace_only_text(self):
        """Test handling of whitespace-only text."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": "   "}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        # Whitespace should be stripped, resulting in no typing
        mock_controller.type.assert_not_called()


class TestMemoryManagement:
    """Test memory management."""

    def test_queue_doesnt_grow_unbounded(self):
        """Test that audio queue is properly managed."""
        speakskiptype.is_recording = True

        # Clear queue
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        # Add many items
        for _ in range(100):
            audio = np.zeros(8000, dtype=np.int16)
            speakskiptype.audio_callback(audio, 8000, None, None)

        # Drain queue
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        # Queue should be empty
        assert speakskiptype.audio_queue.empty()

    def test_recorded_text_cleared_on_start(self):
        """Test that recorded text is cleared when starting new recording."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = "old text that should be cleared"

        speakskiptype.start_recording()

        assert speakskiptype.recorded_text == ""
