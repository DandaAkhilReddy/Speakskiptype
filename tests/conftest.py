"""
Pytest configuration and fixtures for SpeakSkipType tests.
"""

import pytest
import sys
import os
import queue
import json
from unittest.mock import Mock, MagicMock, patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MockKey:
    """Mock Key class for testing keyboard events."""
    ctrl_l = Mock()
    ctrl_r = Mock()
    shift_l = Mock()
    shift_r = Mock()
    ctrl = Mock()


@pytest.fixture
def mock_audio_queue():
    """Provide a fresh queue for audio data."""
    return queue.Queue()


@pytest.fixture
def mock_recognizer():
    """Create a mock Vosk recognizer."""
    recognizer = Mock()
    recognizer.AcceptWaveform = Mock(return_value=True)
    recognizer.Result = Mock(return_value='{"text": "hello world"}')
    recognizer.PartialResult = Mock(return_value='{"partial": "hello"}')
    recognizer.FinalResult = Mock(return_value='{"text": "final text"}')
    return recognizer


@pytest.fixture
def mock_model():
    """Create a mock Vosk model."""
    return Mock()


@pytest.fixture
def mock_keyboard_controller():
    """Create a mock keyboard controller."""
    controller = Mock()
    controller.type = Mock()
    return controller


@pytest.fixture
def sample_audio_data():
    """Provide sample audio data for testing."""
    import numpy as np
    # Generate 1 second of silence at 16kHz
    return np.zeros(16000, dtype=np.int16).tobytes()


@pytest.fixture
def sample_audio_with_noise():
    """Provide sample audio data with noise for testing."""
    import numpy as np
    # Generate 1 second of random noise at 16kHz
    return np.random.randint(-1000, 1000, 16000, dtype=np.int16).tobytes()


@pytest.fixture(autouse=True)
def reset_globals():
    """Reset global variables before each test."""
    # Import the module to reset globals
    import speakskiptype
    speakskiptype.is_recording = False
    speakskiptype.recorded_text = ""
    speakskiptype.ctrl_pressed = False
    speakskiptype.shift_pressed = False
    speakskiptype.hold_to_record_active = False
    speakskiptype.background_mode = False
    speakskiptype.Key = MockKey
    # Clear the audio queue
    while not speakskiptype.audio_queue.empty():
        try:
            speakskiptype.audio_queue.get_nowait()
        except queue.Empty:
            break
    yield


@pytest.fixture
def temp_model_dir(tmp_path):
    """Create a temporary directory for model storage."""
    model_dir = tmp_path / ".speakskiptype"
    model_dir.mkdir()
    return model_dir


@pytest.fixture
def mock_key_class():
    """Create a mock Key class for testing."""
    return MockKey
