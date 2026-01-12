"""
Tests for background mode functionality.
"""

import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class TestBackgroundModeFlag:
    """Tests for background_mode global variable."""

    def test_background_mode_default_false(self):
        """Test that background_mode is False by default."""
        # Reset to default
        speakskiptype.background_mode = False
        assert speakskiptype.background_mode is False

    def test_background_mode_can_be_set_true(self):
        """Test that background_mode can be set to True."""
        speakskiptype.background_mode = True
        assert speakskiptype.background_mode is True
        # Reset
        speakskiptype.background_mode = False


class TestLogFunction:
    """Tests for log() function."""

    def test_log_prints_when_not_background(self, capsys):
        """Test that log() prints when not in background mode."""
        speakskiptype.background_mode = False
        speakskiptype.log("Test message", speakskiptype.Colors.GREEN)
        captured = capsys.readouterr()
        assert "Test message" in captured.out

    def test_log_silent_in_background(self, capsys):
        """Test that log() is silent in background mode."""
        speakskiptype.background_mode = True
        speakskiptype.log("Test message", speakskiptype.Colors.GREEN)
        captured = capsys.readouterr()
        assert captured.out == ""
        # Reset
        speakskiptype.background_mode = False

    def test_log_uses_color(self, capsys):
        """Test that log() uses the provided color."""
        speakskiptype.background_mode = False
        speakskiptype.log("Colored", speakskiptype.Colors.RED)
        captured = capsys.readouterr()
        assert speakskiptype.Colors.RED in captured.out
        assert "Colored" in captured.out

    def test_log_default_color(self, capsys):
        """Test that log() has a default color."""
        speakskiptype.background_mode = False
        speakskiptype.log("Default color")
        captured = capsys.readouterr()
        assert "Default color" in captured.out


class TestNotifyFunction:
    """Tests for notify() function."""

    def test_notify_does_nothing_when_not_background(self):
        """Test that notify() does nothing when not in background mode."""
        speakskiptype.background_mode = False
        # Should not raise any errors
        speakskiptype.notify("Title", "Message")

    @patch('sys.platform', 'win32')
    def test_notify_windows_fallback(self):
        """Test Windows notification fallback."""
        speakskiptype.background_mode = True
        with patch('subprocess.Popen') as mock_popen:
            # Import error for win10toast triggers fallback
            with patch.dict('sys.modules', {'win10toast': None}):
                speakskiptype.notify("Test", "Message")
        # Reset
        speakskiptype.background_mode = False

    @patch('sys.platform', 'darwin')
    def test_notify_macos(self):
        """Test macOS notification."""
        speakskiptype.background_mode = True
        with patch('os.system') as mock_system:
            speakskiptype.notify("Test", "Message")
            # os.system should be called with osascript
        # Reset
        speakskiptype.background_mode = False

    @patch('sys.platform', 'linux')
    def test_notify_linux(self):
        """Test Linux notification."""
        speakskiptype.background_mode = True
        with patch('os.system') as mock_system:
            speakskiptype.notify("Test", "Message")
            # os.system should be called with notify-send
        # Reset
        speakskiptype.background_mode = False

    def test_notify_handles_exceptions(self):
        """Test that notify() handles exceptions gracefully."""
        speakskiptype.background_mode = True
        with patch('sys.platform', 'unknown_platform'):
            # Should not raise
            speakskiptype.notify("Test", "Message")
        # Reset
        speakskiptype.background_mode = False


class TestStartRecordingBackground:
    """Tests for start_recording() in background mode."""

    def test_start_recording_notifies_in_background(self):
        """Test that start_recording sends notification in background mode."""
        speakskiptype.background_mode = True
        speakskiptype.is_recording = False

        with patch.object(speakskiptype, 'notify') as mock_notify:
            speakskiptype.start_recording()
            mock_notify.assert_called_once()
            assert "Recording" in mock_notify.call_args[0][0]

        # Reset
        speakskiptype.background_mode = False
        speakskiptype.is_recording = False

    def test_start_recording_sets_flag_in_background(self):
        """Test that start_recording sets flag in background mode."""
        speakskiptype.background_mode = True
        speakskiptype.is_recording = False

        with patch.object(speakskiptype, 'notify'):
            speakskiptype.start_recording()

        assert speakskiptype.is_recording is True

        # Reset
        speakskiptype.background_mode = False
        speakskiptype.is_recording = False


class TestStopRecordingBackground:
    """Tests for stop_recording_and_type() in background mode."""

    def test_stop_recording_notifies_success_in_background(self):
        """Test notification on successful recognition in background."""
        speakskiptype.background_mode = True
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "hello world"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch.object(speakskiptype, 'notify') as mock_notify:
            with patch('time.sleep'):
                speakskiptype.stop_recording_and_type()

            # Should notify with the text
            assert mock_notify.called
            calls = [str(c) for c in mock_notify.call_args_list]
            assert any("hello world" in str(c) for c in calls)

        # Reset
        speakskiptype.background_mode = False
        speakskiptype.is_recording = False

    def test_stop_recording_notifies_no_speech_in_background(self):
        """Test notification when no speech detected in background."""
        speakskiptype.background_mode = True
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = ""

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch.object(speakskiptype, 'notify') as mock_notify:
            with patch('time.sleep'):
                speakskiptype.stop_recording_and_type()

            # Should notify about no speech
            assert mock_notify.called
            calls = str(mock_notify.call_args_list)
            assert "No Speech" in calls or "No speech" in calls.lower()

        # Reset
        speakskiptype.background_mode = False
        speakskiptype.is_recording = False


class TestAudioCallbackBackground:
    """Tests for audio_callback() in background mode."""

    def test_audio_callback_silent_errors_in_background(self, capsys):
        """Test that audio errors are silent in background mode."""
        speakskiptype.background_mode = True
        speakskiptype.is_recording = True

        # Clear the queue first
        while not speakskiptype.audio_queue.empty():
            speakskiptype.audio_queue.get_nowait()

        # Call with error status
        speakskiptype.audio_callback(b'\x00\x00', 1, None, "Test Error")

        captured = capsys.readouterr()
        # Should not print error in background mode
        assert "Test Error" not in captured.out

        # Reset
        speakskiptype.background_mode = False
        speakskiptype.is_recording = False


class TestProcessAudioBackground:
    """Tests for process_audio() in background mode."""

    def test_process_audio_no_partial_output_in_background(self, capsys):
        """Test that partial results don't print in background mode."""
        speakskiptype.background_mode = True

        mock_recognizer = Mock()
        mock_recognizer.AcceptWaveform.return_value = False
        mock_recognizer.PartialResult.return_value = '{"partial": "testing"}'
        speakskiptype.recognizer = mock_recognizer

        # Add test data and stop signal
        speakskiptype.audio_queue.put(b'\x00\x00')
        speakskiptype.audio_queue.put(None)  # Stop signal

        # Run in thread to avoid blocking
        import threading
        thread = threading.Thread(target=speakskiptype.process_audio)
        thread.start()
        thread.join(timeout=2)

        captured = capsys.readouterr()
        # Should not print partial results in background
        assert "Hearing" not in captured.out

        # Reset
        speakskiptype.background_mode = False


class TestCommandLineArgs:
    """Tests for command line argument parsing."""

    def test_bg_flag_detected(self):
        """Test that --bg flag is detected."""
        with patch.object(sys, 'argv', ['speakskiptype.py', '--bg']):
            assert '--bg' in sys.argv

    def test_background_flag_detected(self):
        """Test that --background flag is detected."""
        with patch.object(sys, 'argv', ['speakskiptype.py', '--background']):
            assert '--background' in sys.argv

    def test_no_flag_is_foreground(self):
        """Test that no flag means foreground mode."""
        with patch.object(sys, 'argv', ['speakskiptype.py']):
            assert '--bg' not in sys.argv
            assert '--background' not in sys.argv


class TestRunBackground:
    """Tests for run_background() function."""

    def test_run_background_sets_flag(self):
        """Test that run_background sets background_mode to True."""
        speakskiptype.background_mode = False

        with patch.object(speakskiptype, 'main_loop'):
            with patch.object(speakskiptype, 'notify'):
                # Mock sys.platform to avoid system tray
                with patch('sys.platform', 'linux'):
                    speakskiptype.run_background()

        assert speakskiptype.background_mode is True

        # Reset
        speakskiptype.background_mode = False

    @patch('sys.platform', 'win32')
    def test_run_background_tries_system_tray_windows(self):
        """Test that Windows tries to create system tray."""
        speakskiptype.background_mode = False

        with patch.object(speakskiptype, 'main_loop'):
            with patch.object(speakskiptype, 'notify'):
                # pystray not available, should fall back
                with patch.dict('sys.modules', {'pystray': None}):
                    speakskiptype.run_background()

        # Reset
        speakskiptype.background_mode = False


class TestMainFunction:
    """Tests for main() function argument handling."""

    def test_main_calls_run_background_with_bg_flag(self):
        """Test that main() calls run_background() with --bg."""
        with patch.object(sys, 'argv', ['speakskiptype.py', '--bg']):
            with patch.object(speakskiptype, 'check_dependencies'):
                with patch.object(speakskiptype, 'run_background') as mock_run_bg:
                    speakskiptype.main()
                    mock_run_bg.assert_called_once()

    def test_main_calls_main_loop_without_flag(self):
        """Test that main() calls main_loop() without --bg."""
        with patch.object(sys, 'argv', ['speakskiptype.py']):
            with patch.object(speakskiptype, 'check_dependencies'):
                with patch.object(speakskiptype, 'print_banner'):
                    with patch.object(speakskiptype, 'main_loop') as mock_main_loop:
                        speakskiptype.main()
                        mock_main_loop.assert_called_once()
