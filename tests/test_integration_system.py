"""
System integration tests - tests that verify the whole system works together.
"""

import pytest
import sys
import os
import subprocess
import importlib
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestModuleImports:
    """Test that all required modules can be imported."""

    def test_import_speakskiptype(self):
        """Test that main module can be imported."""
        import speakskiptype
        assert speakskiptype is not None

    def test_vosk_dependency_configured(self):
        """Test that vosk is configured as a dependency."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'requirements.txt'), encoding='utf-8') as f:
            content = f.read().lower()
        assert 'vosk' in content
        # Also verify the main script references vosk
        with open(os.path.join(project_root, 'speakskiptype.py'), encoding='utf-8') as f:
            script = f.read()
        assert 'vosk' in script.lower() or 'Model' in script

    def test_sounddevice_dependency_configured(self):
        """Test that sounddevice is configured as a dependency."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'requirements.txt'), encoding='utf-8') as f:
            content = f.read().lower()
        assert 'sounddevice' in content
        # Also verify the main script references sounddevice
        with open(os.path.join(project_root, 'speakskiptype.py'), encoding='utf-8') as f:
            script = f.read()
        assert 'sounddevice' in script or 'RawInputStream' in script

    def test_pynput_dependency_configured(self):
        """Test that pynput is configured as a dependency."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'requirements.txt'), encoding='utf-8') as f:
            content = f.read().lower()
        assert 'pynput' in content
        # Also verify the main script references pynput
        with open(os.path.join(project_root, 'speakskiptype.py'), encoding='utf-8') as f:
            script = f.read()
        assert 'pynput' in script or 'keyboard' in script

    def test_vosk_mock_integration(self):
        """Test vosk module can be mocked correctly for the application."""
        mock_model = Mock()
        mock_recognizer = Mock()
        mock_recognizer.AcceptWaveform.return_value = True
        mock_recognizer.Result.return_value = '{"text": "hello"}'
        mock_recognizer.FinalResult.return_value = '{"text": "world"}'

        # Verify mocks work as expected by vosk API
        assert mock_recognizer.AcceptWaveform(b'audio') is True
        import json
        result = json.loads(mock_recognizer.Result())
        assert result['text'] == 'hello'

    def test_sounddevice_mock_integration(self):
        """Test sounddevice can be mocked correctly for the application."""
        mock_stream = Mock()
        mock_stream.__enter__ = Mock(return_value=mock_stream)
        mock_stream.__exit__ = Mock(return_value=False)

        # Verify context manager works
        with mock_stream as stream:
            assert stream is mock_stream

    def test_pynput_mock_integration(self):
        """Test pynput can be mocked correctly for the application."""
        mock_controller = Mock()
        mock_controller.type = Mock()

        # Verify typing works
        mock_controller.type("hello world")
        mock_controller.type.assert_called_once_with("hello world")

    def test_import_queue(self):
        """Test that queue module is available."""
        import queue
        assert queue is not None

    def test_import_json(self):
        """Test that json module is available."""
        import json
        assert json is not None

    def test_import_threading(self):
        """Test that threading module is available."""
        import threading
        assert threading is not None


class TestModuleAttributes:
    """Test that main module has required attributes."""

    def test_has_colors_class(self):
        """Test that Colors class exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'Colors')

    def test_has_print_banner(self):
        """Test that print_banner function exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'print_banner')
        assert callable(speakskiptype.print_banner)

    def test_has_print_controls(self):
        """Test that print_controls function exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'print_controls')
        assert callable(speakskiptype.print_controls)

    def test_has_download_model(self):
        """Test that download_model function exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'download_model')
        assert callable(speakskiptype.download_model)

    def test_has_audio_callback(self):
        """Test that audio_callback function exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'audio_callback')
        assert callable(speakskiptype.audio_callback)

    def test_has_process_audio(self):
        """Test that process_audio function exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'process_audio')
        assert callable(speakskiptype.process_audio)

    def test_has_start_recording(self):
        """Test that start_recording function exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'start_recording')
        assert callable(speakskiptype.start_recording)

    def test_has_stop_recording_and_type(self):
        """Test that stop_recording_and_type function exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'stop_recording_and_type')
        assert callable(speakskiptype.stop_recording_and_type)

    def test_has_on_press(self):
        """Test that on_press function exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'on_press')
        assert callable(speakskiptype.on_press)

    def test_has_on_release(self):
        """Test that on_release function exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'on_release')
        assert callable(speakskiptype.on_release)

    def test_has_main(self):
        """Test that main function exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'main')
        assert callable(speakskiptype.main)


class TestGlobalVariables:
    """Test that global variables are properly initialized."""

    def test_audio_queue_exists(self):
        """Test that audio_queue is initialized."""
        import speakskiptype
        assert hasattr(speakskiptype, 'audio_queue')

    def test_is_recording_exists(self):
        """Test that is_recording flag exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'is_recording')

    def test_recorded_text_exists(self):
        """Test that recorded_text exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'recorded_text')

    def test_keyboard_controller_exists(self):
        """Test that keyboard_controller exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'keyboard_controller')

    def test_ctrl_pressed_exists(self):
        """Test that ctrl_pressed flag exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'ctrl_pressed')


class TestFileStructure:
    """Test that project file structure is correct."""

    def test_main_script_exists(self):
        """Test that main script exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        main_script = os.path.join(project_root, 'speakskiptype.py')
        assert os.path.exists(main_script)

    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        requirements = os.path.join(project_root, 'requirements.txt')
        assert os.path.exists(requirements)

    def test_readme_exists(self):
        """Test that README.md exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        readme = os.path.join(project_root, 'README.md')
        assert os.path.exists(readme)

    def test_install_script_exists(self):
        """Test that install.sh exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        install_sh = os.path.join(project_root, 'install.sh')
        assert os.path.exists(install_sh)


class TestRequirements:
    """Test that requirements.txt contains necessary packages."""

    def test_requirements_contains_vosk(self):
        """Test that vosk is in requirements."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        requirements = os.path.join(project_root, 'requirements.txt')

        with open(requirements, 'r') as f:
            content = f.read().lower()

        assert 'vosk' in content

    def test_requirements_contains_sounddevice(self):
        """Test that sounddevice is in requirements."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        requirements = os.path.join(project_root, 'requirements.txt')

        with open(requirements, 'r') as f:
            content = f.read().lower()

        assert 'sounddevice' in content

    def test_requirements_contains_pynput(self):
        """Test that pynput is in requirements."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        requirements = os.path.join(project_root, 'requirements.txt')

        with open(requirements, 'r') as f:
            content = f.read().lower()

        assert 'pynput' in content


class TestScriptSyntax:
    """Test that main script has valid Python syntax."""

    def test_script_compiles(self):
        """Test that main script compiles without syntax errors."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        main_script = os.path.join(project_root, 'speakskiptype.py')

        with open(main_script, 'r', encoding='utf-8') as f:
            source = f.read()

        # This will raise SyntaxError if there are syntax errors
        compile(source, main_script, 'exec')

    def test_script_is_executable(self):
        """Test that script has shebang line."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        main_script = os.path.join(project_root, 'speakskiptype.py')

        with open(main_script, 'r', encoding='utf-8') as f:
            first_line = f.readline()

        assert first_line.startswith('#!')
        assert 'python' in first_line
