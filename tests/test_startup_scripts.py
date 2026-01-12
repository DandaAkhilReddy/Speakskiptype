"""
Tests for Windows startup scripts.
"""

import os
import sys
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestInstallStartupScript:
    """Tests for install_startup.bat script."""

    def test_install_script_exists(self):
        """Test that install_startup.bat exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'install_startup.bat')
        assert os.path.exists(script_path)

    def test_install_script_is_batch_file(self):
        """Test that install script is a valid batch file."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'install_startup.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert '@echo off' in content.lower()

    def test_install_script_checks_python(self):
        """Test that install script checks for Python."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'install_startup.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert 'python' in content.lower()

    def test_install_script_installs_dependencies(self):
        """Test that install script installs dependencies."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'install_startup.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert 'pip install' in content.lower()
        assert 'vosk' in content
        assert 'sounddevice' in content
        assert 'pynput' in content

    def test_install_script_creates_vbs_launcher(self):
        """Test that install script creates VBS launcher."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'install_startup.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert '.vbs' in content.lower()
        assert 'pythonw' in content.lower()

    def test_install_script_adds_to_startup(self):
        """Test that install script adds to Windows Startup."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'install_startup.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert 'startup' in content.lower()
        assert 'shortcut' in content.lower() or '.lnk' in content.lower()

    def test_install_script_shows_controls(self):
        """Test that install script shows controls."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'install_startup.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert 'ctrl' in content.lower()


class TestUninstallStartupScript:
    """Tests for uninstall_startup.bat script."""

    def test_uninstall_script_exists(self):
        """Test that uninstall_startup.bat exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'uninstall_startup.bat')
        assert os.path.exists(script_path)

    def test_uninstall_script_is_batch_file(self):
        """Test that uninstall script is a valid batch file."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'uninstall_startup.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert '@echo off' in content.lower()

    def test_uninstall_script_kills_process(self):
        """Test that uninstall script kills the process."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'uninstall_startup.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert 'taskkill' in content.lower() or 'kill' in content.lower()

    def test_uninstall_script_removes_startup(self):
        """Test that uninstall script removes from startup."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'uninstall_startup.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert 'del' in content.lower() or 'remove' in content.lower()
        assert 'startup' in content.lower()

    def test_uninstall_script_removes_vbs(self):
        """Test that uninstall script removes VBS file."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'uninstall_startup.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert '.vbs' in content.lower()


class TestStartBackgroundScript:
    """Tests for start_background.bat script."""

    def test_start_script_exists(self):
        """Test that start_background.bat exists."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'start_background.bat')
        assert os.path.exists(script_path)

    def test_start_script_is_batch_file(self):
        """Test that start script is a valid batch file."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'start_background.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert '@echo off' in content.lower()

    def test_start_script_uses_pythonw(self):
        """Test that start script uses pythonw for hidden execution."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'start_background.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert 'pythonw' in content.lower()

    def test_start_script_uses_bg_flag(self):
        """Test that start script uses --bg flag."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'start_background.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert '--bg' in content

    def test_start_script_shows_controls(self):
        """Test that start script shows controls."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'start_background.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert 'ctrl' in content.lower()

    def test_start_script_references_speakskiptype(self):
        """Test that start script references the main script."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'start_background.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert 'speakskiptype.py' in content.lower()


class TestAllScriptsHaveProperLineEndings:
    """Tests for proper file formatting."""

    def test_install_script_no_syntax_errors(self):
        """Test install script has no obvious syntax errors."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'install_startup.bat')

        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Check for balanced quotes
        for i, line in enumerate(lines):
            # Skip comments
            if line.strip().startswith('::') or line.strip().startswith('rem'):
                continue
            # Count quotes (rough check)
            quote_count = line.count('"')
            # Even number of quotes or echo statements (which may have unbalanced)
            if 'echo' not in line.lower():
                assert quote_count % 2 == 0 or '%' in line, f"Unbalanced quotes on line {i+1}"

    def test_scripts_are_readable(self):
        """Test all scripts are readable as text."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        scripts = ['install_startup.bat', 'uninstall_startup.bat', 'start_background.bat']

        for script_name in scripts:
            script_path = os.path.join(project_root, script_name)
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                assert len(content) > 0, f"{script_name} is empty"
            except Exception as e:
                pytest.fail(f"Failed to read {script_name}: {e}")
