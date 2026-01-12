"""
Unit tests for audio processing functionality.
"""

import pytest
import sys
import os
import queue
import json
import numpy as np
from unittest.mock import patch, Mock, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class TestAudioCallback:
    """Test suite for audio_callback function."""

    def test_audio_callback_when_recording(self):
        """Test that audio data is queued when recording."""
        speakskiptype.is_recording = True
        # Clear the queue first
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        test_data = np.array([1, 2, 3, 4], dtype=np.int16)
        speakskiptype.audio_callback(test_data, 4, None, None)

        assert not speakskiptype.audio_queue.empty()
        queued_data = speakskiptype.audio_queue.get()
        assert queued_data == bytes(test_data)

    def test_audio_callback_when_not_recording(self):
        """Test that audio data is NOT queued when not recording."""
        speakskiptype.is_recording = False
        # Clear the queue first
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        test_data = np.array([1, 2, 3, 4], dtype=np.int16)
        speakskiptype.audio_callback(test_data, 4, None, None)

        assert speakskiptype.audio_queue.empty()

    def test_audio_callback_with_status_error(self, capsys):
        """Test that status errors are printed."""
        speakskiptype.is_recording = True
        test_data = np.array([1, 2, 3, 4], dtype=np.int16)

        speakskiptype.audio_callback(test_data, 4, None, "input overflow")

        captured = capsys.readouterr()
        assert "Audio Error" in captured.err or "input overflow" in captured.err

    def test_audio_callback_multiple_calls(self):
        """Test multiple audio callback invocations."""
        speakskiptype.is_recording = True
        # Clear the queue first
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        for i in range(5):
            test_data = np.array([i, i+1, i+2], dtype=np.int16)
            speakskiptype.audio_callback(test_data, 3, None, None)

        count = 0
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()
            count += 1

        assert count == 5


class TestProcessAudio:
    """Test suite for process_audio function."""

    def test_process_audio_recognizes_speech(self):
        """Test that process_audio updates recorded_text on recognition."""
        speakskiptype.recorded_text = ""

        mock_recognizer = Mock()
        mock_recognizer.AcceptWaveform.return_value = True
        mock_recognizer.Result.return_value = '{"text": "hello world"}'
        speakskiptype.recognizer = mock_recognizer

        # Clear and add test data
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        test_data = b'\x00' * 1000
        speakskiptype.audio_queue.put(test_data)
        speakskiptype.audio_queue.put(None)  # Signal to stop

        speakskiptype.process_audio()

        assert "hello world" in speakskiptype.recorded_text

    def test_process_audio_handles_partial_results(self):
        """Test that process_audio handles partial recognition results."""
        mock_recognizer = Mock()
        mock_recognizer.AcceptWaveform.return_value = False
        mock_recognizer.PartialResult.return_value = '{"partial": "hel"}'
        speakskiptype.recognizer = mock_recognizer

        # Clear and add test data
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        test_data = b'\x00' * 1000
        speakskiptype.audio_queue.put(test_data)
        speakskiptype.audio_queue.put(None)  # Signal to stop

        # Should not raise exception
        speakskiptype.process_audio()

    def test_process_audio_stops_on_none(self):
        """Test that process_audio stops when None is received."""
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        speakskiptype.audio_queue.put(None)

        # Should return without hanging
        speakskiptype.process_audio()

    def test_process_audio_empty_text_not_added(self):
        """Test that empty recognition results are not added."""
        speakskiptype.recorded_text = ""

        mock_recognizer = Mock()
        mock_recognizer.AcceptWaveform.return_value = True
        mock_recognizer.Result.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        test_data = b'\x00' * 1000
        speakskiptype.audio_queue.put(test_data)
        speakskiptype.audio_queue.put(None)

        speakskiptype.process_audio()

        assert speakskiptype.recorded_text == ""
