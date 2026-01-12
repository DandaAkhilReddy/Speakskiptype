"""
Integration tests for the complete recording flow.
"""

import pytest
import sys
import os
import queue
import threading
import time
from unittest.mock import patch, Mock, MagicMock
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class MockKey:
    """Mock Key class for testing."""
    ctrl_l = Mock()
    ctrl_r = Mock()


class TestFullRecordingFlow:
    """Integration tests for the complete recording workflow."""

    def setup_method(self):
        """Set up test fixtures."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = ""
        speakskiptype.ctrl_pressed = False
        speakskiptype.Key = MockKey
        # Clear audio queue
        while not speakskiptype.audio_queue.empty():
            try:
                speakskiptype.audio_queue.get_nowait()
            except queue.Empty:
                break

    def test_complete_recording_cycle(self):
        """Test a complete start -> record -> stop -> type cycle."""
        # Setup mocks
        mock_recognizer = Mock()
        mock_recognizer.AcceptWaveform.return_value = True
        mock_recognizer.Result.return_value = '{"text": "hello world"}'
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        # Step 1: Press Ctrl
        speakskiptype.on_press(MockKey.ctrl_l)
        assert speakskiptype.ctrl_pressed is True

        # Step 2: Press R (start recording)
        mock_key_r = Mock()
        mock_key_r.char = 'r'
        speakskiptype.on_press(mock_key_r)
        assert speakskiptype.is_recording is True
        assert speakskiptype.recorded_text == ""

        # Step 3: Simulate audio coming in
        test_audio = np.zeros(8000, dtype=np.int16)
        speakskiptype.audio_callback(test_audio, 8000, None, None)
        assert not speakskiptype.audio_queue.empty()

        # Step 4: Process audio (simulated)
        speakskiptype.recorded_text = "hello world"

        # Step 5: Press S (stop recording)
        mock_key_s = Mock()
        mock_key_s.char = 's'
        with patch('time.sleep'):
            speakskiptype.on_press(mock_key_s)

        # Verify results
        assert speakskiptype.is_recording is False
        mock_controller.type.assert_called_once_with("hello world")

        # Step 6: Release Ctrl
        speakskiptype.on_release(MockKey.ctrl_l)
        assert speakskiptype.ctrl_pressed is False

    def test_recording_cancellation_by_restart(self):
        """Test that starting a new recording doesn't clear ongoing recording."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "ongoing speech"

        # Try to start recording again
        speakskiptype.start_recording()

        # Should NOT clear the text since already recording
        assert speakskiptype.recorded_text == "ongoing speech"
        assert speakskiptype.is_recording is True

    def test_stop_without_start_does_nothing(self):
        """Test that stopping when not recording does nothing harmful."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = "old text"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        speakskiptype.ctrl_pressed = True
        mock_key_s = Mock()
        mock_key_s.char = 's'

        with patch('time.sleep'):
            speakskiptype.on_press(mock_key_s)

        # Should not have typed anything
        mock_controller.type.assert_not_called()

    def test_multiple_recording_sessions(self):
        """Test multiple recording sessions in sequence."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        # Session 1
        speakskiptype.start_recording()
        speakskiptype.recorded_text = "first session"
        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        assert mock_controller.type.call_args_list[0][0][0] == "first session"

        # Session 2
        speakskiptype.start_recording()
        assert speakskiptype.recorded_text == ""  # Should be cleared
        speakskiptype.recorded_text = "second session"
        with patch('time.sleep'):
            speakskiptype.stop_recording_and_type()

        assert mock_controller.type.call_args_list[1][0][0] == "second session"


class TestAudioProcessingIntegration:
    """Integration tests for audio processing pipeline."""

    def setup_method(self):
        """Set up test fixtures."""
        speakskiptype.recorded_text = ""
        while not speakskiptype.audio_queue.empty():
            try:
                speakskiptype.audio_queue.get_nowait()
            except queue.Empty:
                break

    def test_audio_to_text_pipeline(self):
        """Test the complete audio to text pipeline."""
        mock_recognizer = Mock()

        # Simulate partial results followed by final
        call_count = [0]

        def mock_accept(data):
            call_count[0] += 1
            return call_count[0] >= 3  # Return True on 3rd call

        def mock_result():
            return '{"text": "test speech"}'

        def mock_partial():
            return '{"partial": "test"}'

        mock_recognizer.AcceptWaveform = mock_accept
        mock_recognizer.Result = mock_result
        mock_recognizer.PartialResult = mock_partial
        speakskiptype.recognizer = mock_recognizer

        # Add audio chunks
        for i in range(4):
            speakskiptype.audio_queue.put(b'\x00' * 1000)
        speakskiptype.audio_queue.put(None)  # Signal stop

        speakskiptype.process_audio()

        assert "test speech" in speakskiptype.recorded_text

    def test_continuous_audio_callback(self):
        """Test that continuous audio callbacks work correctly."""
        speakskiptype.is_recording = True

        # Clear queue
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        # Simulate continuous audio stream
        for i in range(10):
            audio_chunk = np.random.randint(-100, 100, 1600, dtype=np.int16)
            speakskiptype.audio_callback(audio_chunk, 1600, None, None)

        # Should have 10 chunks in queue
        count = 0
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()
            count += 1

        assert count == 10


class TestKeyboardIntegration:
    """Integration tests for keyboard handling."""

    def setup_method(self):
        """Set up test fixtures."""
        speakskiptype.ctrl_pressed = False
        speakskiptype.is_recording = False
        speakskiptype.Key = MockKey

    def test_rapid_key_presses(self):
        """Test handling of rapid key presses."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        # Rapid Ctrl press/release
        for _ in range(5):
            speakskiptype.on_press(MockKey.ctrl_l)
            speakskiptype.on_release(MockKey.ctrl_l)

        assert speakskiptype.ctrl_pressed is False

    def test_ctrl_held_multiple_commands(self):
        """Test holding Ctrl while pressing multiple command keys."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        # Hold Ctrl
        speakskiptype.on_press(MockKey.ctrl_l)

        # Press R to start
        mock_key_r = Mock()
        mock_key_r.char = 'r'
        speakskiptype.on_press(mock_key_r)
        assert speakskiptype.is_recording is True

        # Still holding Ctrl, press S to stop
        mock_key_s = Mock()
        mock_key_s.char = 's'
        with patch('time.sleep'):
            speakskiptype.on_press(mock_key_s)
        assert speakskiptype.is_recording is False

        # Release Ctrl
        speakskiptype.on_release(MockKey.ctrl_l)
        assert speakskiptype.ctrl_pressed is False
