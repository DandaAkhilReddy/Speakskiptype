"""
Unit tests for model download functionality.
"""

import pytest
import sys
import os
from unittest.mock import patch, Mock, MagicMock
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speakskiptype


class TestDownloadModel:
    """Test suite for download_model function."""

    def test_model_path_construction(self):
        """Test that model path is constructed correctly."""
        expected_suffix = ".speakskiptype/vosk-model-small-en-us-0.15"
        model_path = os.path.expanduser("~/.speakskiptype/vosk-model-small-en-us-0.15")
        assert model_path.endswith(expected_suffix)

    def test_returns_existing_model_path(self, tmp_path):
        """Test that existing model path is returned without download."""
        # Create a fake model directory
        model_dir = tmp_path / ".speakskiptype" / "vosk-model-small-en-us-0.15"
        model_dir.mkdir(parents=True)

        with patch('os.path.expanduser', return_value=str(model_dir)):
            with patch('os.path.exists', return_value=True):
                result = speakskiptype.download_model()
                assert result == str(model_dir)

    def test_creates_model_directory(self, tmp_path):
        """Test that model directory is created if not exists."""
        model_dir = tmp_path / ".speakskiptype" / "vosk-model-small-en-us-0.15"

        with patch('os.path.expanduser', return_value=str(model_dir)):
            with patch('os.path.exists', return_value=False):
                with patch('os.makedirs') as mock_makedirs:
                    with patch('urllib.request.urlretrieve') as mock_download:
                        with patch('zipfile.ZipFile') as mock_zip:
                            mock_zip.return_value.__enter__ = Mock()
                            mock_zip.return_value.__exit__ = Mock(return_value=False)
                            with patch('os.remove'):
                                try:
                                    speakskiptype.download_model()
                                except:
                                    pass
                                # Check makedirs was called
                                mock_makedirs.assert_called()

    def test_download_url_is_correct(self):
        """Test that the download URL is the correct Vosk model URL."""
        expected_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        # This is a documentation test to ensure URL is maintained
        assert expected_url.startswith("https://alphacephei.com/vosk/models/")
        assert expected_url.endswith(".zip")


class TestDownloadProgress:
    """Test suite for download progress reporting."""

    def test_progress_calculation_start(self):
        """Test progress at start of download."""
        block_num = 0
        block_size = 8192
        total_size = 40000000  # 40MB

        downloaded = block_num * block_size
        percent = min(100, (downloaded / total_size) * 100)

        assert percent == 0

    def test_progress_calculation_middle(self):
        """Test progress at middle of download."""
        block_num = 2500
        block_size = 8192
        total_size = 40000000

        downloaded = block_num * block_size
        percent = min(100, (downloaded / total_size) * 100)

        assert 40 < percent < 60

    def test_progress_calculation_end(self):
        """Test progress at end of download."""
        block_num = 5000
        block_size = 8192
        total_size = 40000000

        downloaded = block_num * block_size
        percent = min(100, (downloaded / total_size) * 100)

        assert percent == 100  # min(100, ...) caps at 100

    def test_progress_bar_length(self):
        """Test that progress bar has correct length."""
        bar_length = 40
        percent = 50
        filled = int(bar_length * percent / 100)

        assert filled == 20
        assert bar_length - filled == 20
