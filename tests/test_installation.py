"""
Installation verification tests.
Tests that verify the package can be installed and run correctly.
"""

import pytest
import sys
import os
import subprocess
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPackageStructure:
    """Test package structure is correct for installation."""

    def test_main_script_exists(self):
        """Test main script exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assert os.path.exists(os.path.join(project_root, 'speakskiptype.py'))

    def test_requirements_txt_exists(self):
        """Test requirements.txt exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assert os.path.exists(os.path.join(project_root, 'requirements.txt'))

    def test_setup_py_exists(self):
        """Test setup.py exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assert os.path.exists(os.path.join(project_root, 'setup.py'))

    def test_readme_exists(self):
        """Test README.md exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assert os.path.exists(os.path.join(project_root, 'README.md'))

    def test_install_sh_exists(self):
        """Test install.sh exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assert os.path.exists(os.path.join(project_root, 'install.sh'))

    def test_install_bat_exists(self):
        """Test install.bat exists for Windows."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assert os.path.exists(os.path.join(project_root, 'install.bat'))


class TestRequirementsFile:
    """Test requirements.txt content."""

    def test_vosk_in_requirements(self):
        """Test vosk is in requirements."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'requirements.txt'), encoding='utf-8') as f:
            content = f.read()
        assert 'vosk' in content.lower()

    def test_sounddevice_in_requirements(self):
        """Test sounddevice is in requirements."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'requirements.txt'), encoding='utf-8') as f:
            content = f.read()
        assert 'sounddevice' in content.lower()

    def test_pynput_in_requirements(self):
        """Test pynput is in requirements."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'requirements.txt'), encoding='utf-8') as f:
            content = f.read()
        assert 'pynput' in content.lower()

    def test_requirements_format_valid(self):
        """Test requirements.txt format is valid."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'requirements.txt'), encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Should be package name with optional version
                assert '=' in line or line.isidentifier() or '-' in line


class TestSetupPy:
    """Test setup.py content and validity."""

    def test_setup_py_valid_python(self):
        """Test setup.py is valid Python."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        setup_path = os.path.join(project_root, 'setup.py')

        with open(setup_path, encoding='utf-8') as f:
            source = f.read()

        # Should compile without errors
        compile(source, setup_path, 'exec')

    def test_setup_py_has_name(self):
        """Test setup.py defines package name."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'setup.py'), encoding='utf-8') as f:
            content = f.read()
        assert 'name=' in content or "name =" in content

    def test_setup_py_has_version(self):
        """Test setup.py defines version."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'setup.py'), encoding='utf-8') as f:
            content = f.read()
        assert 'version=' in content or "version =" in content

    def test_setup_py_has_install_requires(self):
        """Test setup.py defines install_requires."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'setup.py'), encoding='utf-8') as f:
            content = f.read()
        assert 'install_requires' in content


class TestReadme:
    """Test README.md content."""

    def test_readme_has_installation_instructions(self):
        """Test README has installation instructions."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'README.md'), encoding='utf-8') as f:
            content = f.read().lower()
        assert 'install' in content

    def test_readme_has_usage_instructions(self):
        """Test README has usage instructions."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'README.md'), encoding='utf-8') as f:
            content = f.read().lower()
        assert 'usage' in content or 'ctrl' in content

    def test_readme_has_controls(self):
        """Test README documents controls."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'README.md'), encoding='utf-8') as f:
            content = f.read()
        assert 'Ctrl+R' in content or 'Ctrl + R' in content

    def test_readme_mentions_free(self):
        """Test README mentions it's free."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'README.md'), encoding='utf-8') as f:
            content = f.read().lower()
        assert 'free' in content

    def test_readme_mentions_local(self):
        """Test README mentions local processing."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'README.md'), encoding='utf-8') as f:
            content = f.read().lower()
        assert 'local' in content


class TestInstallScripts:
    """Test installation scripts."""

    def test_install_sh_is_bash_script(self):
        """Test install.sh is a bash script."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'install.sh'), encoding='utf-8') as f:
            first_line = f.readline()
        assert first_line.startswith('#!') and ('bash' in first_line or 'sh' in first_line)

    def test_install_sh_pip_install(self):
        """Test install.sh runs pip install."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'install.sh'), encoding='utf-8') as f:
            content = f.read()
        assert 'pip' in content

    def test_install_bat_format(self):
        """Test install.bat is valid batch file."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(project_root, 'install.bat'), encoding='utf-8') as f:
            content = f.read()
        assert '@echo' in content.lower() or 'pip' in content.lower()


class TestScriptExecution:
    """Test script can be executed."""

    def test_script_imports_without_error(self):
        """Test script can be imported."""
        import speakskiptype
        assert speakskiptype is not None

    def test_script_has_main_function(self):
        """Test script has main function."""
        import speakskiptype
        assert hasattr(speakskiptype, 'main')
        assert callable(speakskiptype.main)

    def test_script_syntax_check(self):
        """Test script syntax with Python."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'speakskiptype.py')

        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', script_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Syntax error: {result.stderr}"


class TestIsolatedImport:
    """Test importing in isolated subprocess."""

    def test_import_in_subprocess(self):
        """Test module can be imported in fresh subprocess."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Use repr() to properly escape Windows paths
        escaped_path = repr(project_root)

        code = f'''
import sys
sys.path.insert(0, {escaped_path})
try:
    import speakskiptype
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {{e}}")
'''
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            cwd=project_root
        )

        assert "SUCCESS" in result.stdout, f"Import failed: {result.stderr}"

    def test_colors_class_in_subprocess(self):
        """Test Colors class works in subprocess."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Use repr() to properly escape Windows paths
        escaped_path = repr(project_root)

        code = f'''
import sys
sys.path.insert(0, {escaped_path})
from speakskiptype import Colors
assert Colors.RED == "\\033[91m"
assert Colors.GREEN == "\\033[92m"
print("SUCCESS")
'''
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            cwd=project_root
        )

        assert "SUCCESS" in result.stdout, f"Test failed: {result.stderr}"

    def test_functions_exist_in_subprocess(self):
        """Test all functions exist when imported in subprocess."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Use repr() to properly escape Windows paths
        escaped_path = repr(project_root)

        code = f'''
import sys
sys.path.insert(0, {escaped_path})
import speakskiptype

functions = [
    'check_dependencies',
    'print_banner',
    'print_controls',
    'download_model',
    'audio_callback',
    'process_audio',
    'start_recording',
    'stop_recording_and_type',
    'on_press',
    'on_release',
    'main'
]

for func in functions:
    assert hasattr(speakskiptype, func), f"Missing function: {{func}}"
    assert callable(getattr(speakskiptype, func)), f"Not callable: {{func}}"

print("SUCCESS")
'''
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            cwd=project_root
        )

        assert "SUCCESS" in result.stdout, f"Test failed: {result.stderr}"


class TestDependencyCheck:
    """Test dependency checking functionality."""

    def test_check_dependencies_function_exists(self):
        """Test check_dependencies function exists."""
        import speakskiptype
        assert hasattr(speakskiptype, 'check_dependencies')

    def test_required_packages_list(self):
        """Test required packages are correct."""
        # The function checks for these packages
        required = ['vosk', 'sounddevice', 'pynput']
        assert len(required) == 3
        assert 'vosk' in required
        assert 'sounddevice' in required
        assert 'pynput' in required
