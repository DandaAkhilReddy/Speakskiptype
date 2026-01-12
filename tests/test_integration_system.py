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


def _can_import(module_name):
    """Check if a module can be imported."""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


class TestModuleImports:
    """Test that all required modules can be imported."""

    def test_import_speakskiptype(self):
        """Test that main module can be imported."""
        import speakskiptype
        assert speakskiptype is not None

    @pytest.mark.skipif(not _can_import('vosk'), reason="vosk not installed")
    def test_import_vosk(self):
        """Test that vosk can be imported."""
        import vosk
        assert vosk is not None

    @pytest.mark.skipif(not _can_import('sounddevice'), reason="sounddevice not installed")
    def test_import_sounddevice(self):
        """Test that sounddevice can be imported."""
        import sounddevice
        assert sounddevice is not None

    @pytest.mark.skipif(not _can_import('pynput'), reason="pynput not installed")
    def test_import_pynput(self):
        """Test that pynput can be imported."""
        import pynput
        assert pynput is not None

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

        with open(main_script, 'r') as f:
            source = f.read()

        # This will raise SyntaxError if there are syntax errors
        compile(source, main_script, 'exec')

    def test_script_is_executable(self):
        """Test that script has shebang line."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        main_script = os.path.join(project_root, 'speakskiptype.py')

        with open(main_script, 'r') as f:
            first_line = f.readline()

        assert first_line.startswith('#!')
        assert 'python' in first_line
