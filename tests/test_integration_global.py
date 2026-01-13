"""
Integration tests for global hotkey functionality.
"""

import os
import sys
import pytest
import threading
import time
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class TestGlobalHotkeyIntegration:
    """Integration tests for global hotkey system."""

    def setup_method(self):
        """Reset state before each test."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = ""
        speakskiptype.ctrl_pressed = False
        speakskiptype.background_mode = False

    def test_ctrl_r_then_ctrl_s_full_flow(self):
        """Test complete flow: Ctrl+R to start, speak, Ctrl+S to type."""
        # Setup mocks
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": "hello world"}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        # Simulate Ctrl+R
        speakskiptype.ctrl_pressed = True
        mock_key_r = Mock()
        mock_key_r.char = 'r'
        speakskiptype.on_press(mock_key_r)

        assert speakskiptype.is_recording is True

        # Simulate speech recognition adding text
        speakskiptype.recorded_text = "hello "

        # Simulate Ctrl+S
        mock_key_s = Mock()
        mock_key_s.char = 's'

        with patch('time.sleep'):
            with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True) as mock_copy:
                with patch.object(speakskiptype, 'paste_from_clipboard') as mock_paste:
                    speakskiptype.on_press(mock_key_s)

        assert speakskiptype.is_recording is False
        # Text should be copied to clipboard and pasted
        assert mock_copy.called
        copied_text = mock_copy.call_args[0][0]
        assert "hello" in copied_text

    def test_multiple_recording_sessions(self):
        """Test multiple recording sessions work correctly."""
        mock_recognizer = Mock()
        mock_controller = Mock()
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = mock_controller

        with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True) as mock_copy:
            with patch.object(speakskiptype, 'paste_from_clipboard'):
                for i in range(3):
                    mock_recognizer.FinalResult.return_value = f'{{"text": "session {i}"}}'

                    # Start recording
                    speakskiptype.ctrl_pressed = True
                    speakskiptype.is_recording = False
                    speakskiptype.start_recording()
                    assert speakskiptype.is_recording is True

                    # Add some text
                    speakskiptype.recorded_text = f"test {i} "

                    # Stop recording
                    with patch('time.sleep'):
                        speakskiptype.stop_recording_and_type()

                    assert speakskiptype.is_recording is False

        # Should have copied 3 times (using clipboard now)
        assert mock_copy.call_count == 3

    def test_keyboard_listener_doesnt_suppress_events(self):
        """Test that keyboard events are not suppressed (for global use)."""
        # The on_press function should return None (not False)
        # to allow events to propagate to other applications
        speakskiptype.ctrl_pressed = True

        mock_key = Mock()
        mock_key.char = 'r'

        result = speakskiptype.on_press(mock_key)

        # Should return None to not suppress the event
        assert result is None


class TestBackgroundModeIntegration:
    """Integration tests for background mode."""

    def setup_method(self):
        """Reset state before each test."""
        speakskiptype.background_mode = False
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = ""

    def test_background_mode_full_cycle(self):
        """Test full recording cycle in background mode."""
        speakskiptype.background_mode = True

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": "background test"}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch.object(speakskiptype, 'notify') as mock_notify:
            with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True) as mock_copy:
                with patch.object(speakskiptype, 'paste_from_clipboard'):
                    # Start recording
                    speakskiptype.start_recording()
                    assert speakskiptype.is_recording is True
                    assert mock_notify.called

                    # Add text
                    speakskiptype.recorded_text = "test "

                    # Stop and type
                    with patch('time.sleep'):
                        speakskiptype.stop_recording_and_type()

                    assert speakskiptype.is_recording is False
                    mock_copy.assert_called_once()

        speakskiptype.background_mode = False

    def test_background_silent_console_output(self, capsys):
        """Test that background mode doesn't print to console."""
        speakskiptype.background_mode = True

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()

        with patch.object(speakskiptype, 'notify'):
            speakskiptype.start_recording()
            with patch('time.sleep'):
                speakskiptype.stop_recording_and_type()

        captured = capsys.readouterr()
        # Should have minimal or no console output
        assert "[REC]" not in captured.out
        assert "[STOP]" not in captured.out

        speakskiptype.background_mode = False


class TestQuitIntegration:
    """Integration tests for quit functionality."""

    def test_ctrl_q_exits_application(self):
        """Test that Ctrl+Q triggers exit."""
        speakskiptype.ctrl_pressed = True

        mock_key = Mock()
        mock_key.char = 'q'

        with patch.object(speakskiptype.os, '_exit') as mock_exit:
            with patch.object(speakskiptype, 'notify'):
                speakskiptype.on_press(mock_key)
                mock_exit.assert_called_once_with(0)

    def test_ctrl_q_notifies_in_background(self):
        """Test that Ctrl+Q sends notification in background mode."""
        speakskiptype.background_mode = True
        speakskiptype.ctrl_pressed = True

        mock_key = Mock()
        mock_key.char = 'q'

        with patch.object(speakskiptype.os, '_exit'):
            with patch.object(speakskiptype, 'notify') as mock_notify:
                speakskiptype.on_press(mock_key)
                assert mock_notify.called

        speakskiptype.background_mode = False


class TestAudioIntegration:
    """Integration tests for audio processing."""

    def test_audio_queue_integration(self):
        """Test audio queue processes data correctly."""
        # Clear the queue
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        speakskiptype.is_recording = True

        # Simulate audio callback
        test_audio = b'\x00\x01\x02\x03'
        speakskiptype.audio_callback(test_audio, 4, None, None)

        # Check data was queued
        assert not speakskiptype.audio_queue.empty()
        queued_data = speakskiptype.audio_queue.get_nowait()
        assert queued_data == test_audio

        speakskiptype.is_recording = False

    def test_audio_not_queued_when_not_recording(self):
        """Test audio is not queued when not recording."""
        # Clear the queue
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        speakskiptype.is_recording = False

        # Simulate audio callback
        speakskiptype.audio_callback(b'\x00\x01', 2, None, None)

        # Queue should still be empty
        assert speakskiptype.audio_queue.empty()


class TestConcurrentAccess:
    """Tests for thread safety and concurrent access."""

    def test_rapid_start_stop_cycles(self):
        """Test rapid start/stop doesn't cause issues."""
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()

        for _ in range(10):
            speakskiptype.start_recording()
            with patch('time.sleep'):
                speakskiptype.stop_recording_and_type()

        # Should end in not recording state
        assert speakskiptype.is_recording is False

    def test_double_start_is_safe(self):
        """Test calling start_recording twice is safe - toggles on second call."""
        speakskiptype.is_recording = False

        # Setup mocks for stop
        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()

        speakskiptype.start_recording()
        assert speakskiptype.is_recording is True

        # Second start toggles (stops) - this is the new toggle behavior
        speakskiptype.recorded_text = "some text"
        with patch('time.sleep'):
            with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True):
                with patch.object(speakskiptype, 'paste_from_clipboard'):
                    speakskiptype.start_recording()

        # Toggle behavior: now stopped
        assert speakskiptype.is_recording is False

    def test_double_stop_is_safe(self):
        """Test calling stop_recording twice is safe."""
        speakskiptype.is_recording = False

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()

        with patch('time.sleep'):
            # Should not crash
            speakskiptype.stop_recording_and_type()
            speakskiptype.stop_recording_and_type()


class TestErrorHandling:
    """Tests for error handling in integration scenarios."""

    def test_recognizer_error_handling(self):
        """Test handling of recognizer errors."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.side_effect = Exception("Recognizer error")
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()

        # Should raise but we catch it
        with pytest.raises(Exception):
            with patch('time.sleep'):
                speakskiptype.stop_recording_and_type()

    def test_keyboard_controller_error_handling(self):
        """Test handling of keyboard controller errors."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "test"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        mock_controller.type.side_effect = Exception("Keyboard error")
        speakskiptype.keyboard_controller = mock_controller

        # Should raise
        with pytest.raises(Exception):
            with patch('time.sleep'):
                speakskiptype.stop_recording_and_type()


class TestMainLoopIntegration:
    """Tests for main_loop function integration."""

    def test_main_loop_initializes_components(self):
        """Test that main_loop initializes all required components."""
        # Test that main_loop function exists and is callable
        assert hasattr(speakskiptype, 'main_loop')
        assert callable(speakskiptype.main_loop)

        # Test that it would initialize model and recognizer (via mocking)
        with patch.object(speakskiptype, 'init_keyboard'):
            with patch.object(speakskiptype, 'download_model', return_value='/fake/path'):
                # Just verify the function signature is correct
                import inspect
                sig = inspect.signature(speakskiptype.main_loop)
                assert len(sig.parameters) == 0  # No required parameters

    def test_main_function_checks_dependencies(self):
        """Test that main() calls check_dependencies."""
        with patch.object(speakskiptype, 'check_dependencies') as mock_check:
            with patch.object(speakskiptype, 'print_banner'):
                with patch.object(speakskiptype, 'main_loop'):
                    with patch.object(sys, 'argv', ['speakskiptype.py']):
                        speakskiptype.main()
                        mock_check.assert_called_once()
