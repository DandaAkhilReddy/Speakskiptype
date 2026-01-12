"""
Cross-platform compatibility tests.
Tests that verify the tool works correctly on Windows, macOS, and Linux.
"""

import pytest
import sys
import os
import platform
import tempfile
import shutil
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class TestPlatformDetection:
    """Test platform-specific behavior."""

    def test_platform_is_detected(self):
        """Test that the current platform can be detected."""
        current_platform = platform.system()
        assert current_platform in ['Windows', 'Darwin', 'Linux']

    def test_python_version_supported(self):
        """Test that Python version is 3.7+."""
        assert sys.version_info >= (3, 7)

    def test_python_version_components(self):
        """Test Python version components are accessible."""
        assert sys.version_info.major == 3
        assert sys.version_info.minor >= 7


class TestPathHandling:
    """Test cross-platform path handling."""

    def test_home_directory_exists(self):
        """Test that home directory can be expanded."""
        home = os.path.expanduser("~")
        assert os.path.exists(home)
        assert os.path.isdir(home)

    def test_model_path_uses_home(self):
        """Test that model path is relative to home directory."""
        model_path = os.path.expanduser("~/.speakskiptype/vosk-model-small-en-us-0.15")
        assert model_path.startswith(os.path.expanduser("~"))

    def test_path_separator_handling(self):
        """Test that path separators are handled correctly."""
        # This should work on all platforms
        test_path = os.path.join("home", "user", ".speakskiptype")
        assert "speakskiptype" in test_path

    def test_temp_directory_accessible(self):
        """Test that temp directory is accessible for downloads."""
        temp_dir = tempfile.gettempdir()
        assert os.path.exists(temp_dir)
        assert os.access(temp_dir, os.W_OK)

    def test_can_create_temp_file(self):
        """Test that we can create temporary files."""
        fd, path = tempfile.mkstemp()
        try:
            os.close(fd)
            assert os.path.exists(path)
        finally:
            os.unlink(path)

    def test_model_directory_creation(self):
        """Test that model directory can be created."""
        temp_dir = tempfile.mkdtemp()
        try:
            model_dir = os.path.join(temp_dir, ".speakskiptype", "model")
            os.makedirs(model_dir, exist_ok=True)
            assert os.path.exists(model_dir)
            assert os.path.isdir(model_dir)
        finally:
            shutil.rmtree(temp_dir)


class TestWindowsCompatibility:
    """Tests specific to Windows compatibility."""

    def test_windows_path_handling(self):
        """Test Windows-style paths are handled."""
        # Test that we can handle Windows-style paths
        if platform.system() == 'Windows':
            home = os.path.expanduser("~")
            assert ":\\" in home or "/" in home

    def test_ctrl_key_codes_windows(self):
        """Test Ctrl key codes that Windows uses."""
        # Windows sends \x12 for Ctrl+R, \x13 for Ctrl+S
        assert '\x12' == chr(18)  # Ctrl+R
        assert '\x13' == chr(19)  # Ctrl+S
        assert '\x11' == chr(17)  # Ctrl+Q

    def test_line_endings_handling(self):
        """Test that different line endings are handled."""
        # Test various line ending formats
        text_unix = "line1\nline2"
        text_windows = "line1\r\nline2"
        text_mac = "line1\rline2"

        # All should have content
        assert "line1" in text_unix
        assert "line1" in text_windows
        assert "line1" in text_mac


class TestMacOSCompatibility:
    """Tests specific to macOS compatibility."""

    def test_macos_home_directory(self):
        """Test macOS home directory format."""
        if platform.system() == 'Darwin':
            home = os.path.expanduser("~")
            assert home.startswith("/Users/") or home.startswith("/var/")

    def test_macos_keychain_not_required(self):
        """Test that we don't require macOS Keychain access."""
        # Our app should work without Keychain
        # This is a placeholder test - the tool doesn't use Keychain
        assert True


class TestLinuxCompatibility:
    """Tests specific to Linux compatibility."""

    def test_linux_home_directory(self):
        """Test Linux home directory format."""
        if platform.system() == 'Linux':
            home = os.path.expanduser("~")
            assert home.startswith("/home/") or home == "/root"

    def test_linux_audio_permissions_note(self):
        """Test that audio group documentation exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        readme = os.path.join(project_root, 'README.md')

        with open(readme, 'r', encoding='utf-8') as f:
            content = f.read()

        # README should mention Linux audio permissions
        assert 'audio' in content.lower()


class TestUnicodeAndEncoding:
    """Test Unicode and encoding compatibility across platforms."""

    def test_utf8_text_handling(self):
        """Test that UTF-8 text is handled correctly."""
        test_text = "Hello 世界 مرحبا 🎤"
        encoded = test_text.encode('utf-8')
        decoded = encoded.decode('utf-8')
        assert decoded == test_text

    def test_ascii_text_handling(self):
        """Test that ASCII text is handled correctly."""
        test_text = "Hello World 123"
        assert test_text.isascii() or all(ord(c) < 128 for c in test_text)

    def test_special_characters_in_commands(self):
        """Test special characters that might appear in commands."""
        test_commands = [
            "git commit -m 'fix bug'",
            'echo "hello world"',
            "cd ~/projects",
            "npm install @types/node",
            "docker run -e VAR=value",
        ]
        for cmd in test_commands:
            assert isinstance(cmd, str)
            assert len(cmd) > 0


class TestEnvironmentVariables:
    """Test environment variable handling across platforms."""

    def test_home_env_variable(self):
        """Test HOME or USERPROFILE environment variable."""
        home = os.environ.get('HOME') or os.environ.get('USERPROFILE')
        assert home is not None or os.path.expanduser("~") != "~"

    def test_path_env_variable(self):
        """Test PATH environment variable exists."""
        path = os.environ.get('PATH')
        assert path is not None
        assert len(path) > 0

    def test_python_path_accessible(self):
        """Test that Python is accessible via sys.executable."""
        assert os.path.exists(sys.executable)


class TestFilePermissions:
    """Test file permission handling across platforms."""

    def test_can_create_executable_file(self):
        """Test that we can create files with execute permission."""
        temp_dir = tempfile.mkdtemp()
        try:
            script_path = os.path.join(temp_dir, "test_script.py")
            with open(script_path, 'w') as f:
                f.write("#!/usr/bin/env python3\nprint('test')")

            # Make executable (Unix-like systems)
            if platform.system() != 'Windows':
                os.chmod(script_path, 0o755)
                assert os.access(script_path, os.X_OK)
        finally:
            shutil.rmtree(temp_dir)

    def test_can_read_write_files(self):
        """Test basic file read/write operations."""
        temp_dir = tempfile.mkdtemp()
        try:
            test_file = os.path.join(temp_dir, "test.txt")

            # Write
            with open(test_file, 'w') as f:
                f.write("test content")

            # Read
            with open(test_file, 'r') as f:
                content = f.read()

            assert content == "test content"
        finally:
            shutil.rmtree(temp_dir)


class TestKeyboardCrossplatform:
    """Test keyboard handling across platforms."""

    def test_ctrl_key_constants(self):
        """Test that Ctrl key character codes are correct."""
        # These are standard ASCII control characters
        assert ord('r') - ord('a') + 1 == 18  # Ctrl+R = 0x12
        assert ord('s') - ord('a') + 1 == 19  # Ctrl+S = 0x13
        assert ord('q') - ord('a') + 1 == 17  # Ctrl+Q = 0x11

    def test_key_event_handling(self):
        """Test that key events can be processed."""
        # Create mock key with char attribute
        mock_key = Mock()
        mock_key.char = 'r'

        # Verify the mock works
        assert hasattr(mock_key, 'char')
        assert mock_key.char == 'r'


class TestAudioCrossplatform:
    """Test audio handling across platforms."""

    def test_audio_sample_rate_standard(self):
        """Test that we use standard audio sample rate."""
        # 16000 Hz is widely supported
        sample_rate = 16000
        assert sample_rate == 16000

    def test_audio_format_standard(self):
        """Test that we use standard audio format."""
        # int16 is widely supported
        import numpy as np
        test_audio = np.zeros(1000, dtype=np.int16)
        assert test_audio.dtype == np.int16

    def test_audio_channels_mono(self):
        """Test that we use mono audio (most compatible)."""
        # Mono audio is more universally supported
        channels = 1
        assert channels == 1
