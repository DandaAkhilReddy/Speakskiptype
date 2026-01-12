"""
Tests for clipboard functionality.
"""

import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class TestCopyToClipboard:
    """Tests for copy_to_clipboard function."""

    def test_copy_to_clipboard_exists(self):
        """Test that copy_to_clipboard function exists."""
        assert hasattr(speakskiptype, 'copy_to_clipboard')
        assert callable(speakskiptype.copy_to_clipboard)

    @patch('sys.platform', 'win32')
    def test_copy_to_clipboard_windows(self):
        """Test Windows clipboard copy."""
        with patch('subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.communicate.return_value = (None, None)
            mock_popen.return_value = mock_process

            result = speakskiptype.copy_to_clipboard("test text")

            assert result is True
            mock_popen.assert_called_once()
            # Check that clip was called
            args = mock_popen.call_args
            assert 'clip' in str(args)

    @patch('sys.platform', 'darwin')
    def test_copy_to_clipboard_macos(self):
        """Test macOS clipboard copy."""
        with patch('subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.communicate.return_value = (None, None)
            mock_popen.return_value = mock_process

            result = speakskiptype.copy_to_clipboard("test text")

            assert result is True
            mock_popen.assert_called_once()
            args = mock_popen.call_args
            assert 'pbcopy' in str(args)

    @patch('sys.platform', 'linux')
    def test_copy_to_clipboard_linux_xclip(self):
        """Test Linux clipboard copy with xclip."""
        with patch('subprocess.Popen') as mock_popen:
            mock_process = Mock()
            mock_process.communicate.return_value = (None, None)
            mock_popen.return_value = mock_process

            result = speakskiptype.copy_to_clipboard("test text")

            assert result is True
            args = mock_popen.call_args
            assert 'xclip' in str(args)

    @patch('sys.platform', 'linux')
    def test_copy_to_clipboard_linux_fallback_xsel(self):
        """Test Linux clipboard fallback to xsel."""
        call_count = [0]

        def mock_popen_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                raise FileNotFoundError("xclip not found")
            mock_process = Mock()
            mock_process.communicate.return_value = (None, None)
            return mock_process

        with patch('subprocess.Popen', side_effect=mock_popen_side_effect):
            result = speakskiptype.copy_to_clipboard("test text")
            assert result is True

    @patch('sys.platform', 'linux')
    def test_copy_to_clipboard_linux_no_clipboard_tool(self):
        """Test Linux returns False when no clipboard tool available."""
        def mock_popen_fail(*args, **kwargs):
            raise FileNotFoundError("No clipboard tool")

        with patch('subprocess.Popen', side_effect=mock_popen_fail):
            result = speakskiptype.copy_to_clipboard("test text")
            assert result is False


class TestPasteFromClipboard:
    """Tests for paste_from_clipboard function."""

    def test_paste_from_clipboard_exists(self):
        """Test that paste_from_clipboard function exists."""
        assert hasattr(speakskiptype, 'paste_from_clipboard')
        assert callable(speakskiptype.paste_from_clipboard)

    def test_paste_simulates_ctrl_v(self):
        """Test that paste simulates Ctrl+V."""
        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        # Need to set Key
        mock_key = Mock()
        mock_key.ctrl = 'ctrl'
        speakskiptype.Key = mock_key

        with patch('time.sleep'):
            speakskiptype.paste_from_clipboard()

        # Should press and release ctrl and v
        assert mock_controller.press.called
        assert mock_controller.release.called
        # Check v was pressed
        calls = [str(c) for c in mock_controller.press.call_args_list]
        assert any('v' in c for c in calls)


class TestStopRecordingWithClipboard:
    """Tests for stop_recording_and_type with clipboard."""

    def setup_method(self):
        """Reset state before each test."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = ""
        speakskiptype.background_mode = False

    def test_stop_recording_uses_clipboard(self):
        """Test that stop_recording uses clipboard method."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "hello world"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True) as mock_copy:
            with patch.object(speakskiptype, 'paste_from_clipboard') as mock_paste:
                with patch('time.sleep'):
                    speakskiptype.stop_recording_and_type()

                mock_copy.assert_called_once_with("hello world")
                mock_paste.assert_called_once()

    def test_stop_recording_fallback_to_type(self):
        """Test fallback to keyboard typing when clipboard fails."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "fallback test"

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        with patch.object(speakskiptype, 'copy_to_clipboard', return_value=False):
            with patch('time.sleep'):
                speakskiptype.stop_recording_and_type()

        # Should fall back to type method
        mock_controller.type.assert_called_once_with("fallback test")

    def test_stop_recording_logs_paste_message(self, capsys):
        """Test that stop_recording logs 'Pasting' message."""
        speakskiptype.is_recording = True
        speakskiptype.recorded_text = "test"
        speakskiptype.background_mode = False

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": ""}'
        speakskiptype.recognizer = mock_recognizer
        speakskiptype.keyboard_controller = Mock()

        with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True):
            with patch.object(speakskiptype, 'paste_from_clipboard'):
                with patch('time.sleep'):
                    speakskiptype.stop_recording_and_type()

        captured = capsys.readouterr()
        assert "PASTE" in captured.out or "Pasting" in captured.out


class TestClipboardIntegration:
    """Integration tests for clipboard functionality."""

    def test_full_recording_cycle_with_clipboard(self):
        """Test complete recording cycle uses clipboard."""
        speakskiptype.is_recording = False
        speakskiptype.recorded_text = ""

        mock_recognizer = Mock()
        mock_recognizer.FinalResult.return_value = '{"text": "integration test"}'
        speakskiptype.recognizer = mock_recognizer

        mock_controller = Mock()
        speakskiptype.keyboard_controller = mock_controller

        # Start recording
        speakskiptype.start_recording()
        assert speakskiptype.is_recording is True

        # Simulate some recognized text
        speakskiptype.recorded_text = "hello "

        # Stop recording
        with patch.object(speakskiptype, 'copy_to_clipboard', return_value=True) as mock_copy:
            with patch.object(speakskiptype, 'paste_from_clipboard') as mock_paste:
                with patch('time.sleep'):
                    speakskiptype.stop_recording_and_type()

        assert speakskiptype.is_recording is False
        # Should have used clipboard
        assert mock_copy.called
        # Text should include both recorded and final
        copied_text = mock_copy.call_args[0][0]
        assert "hello" in copied_text or "integration" in copied_text
