"""Test CLI module imports"""

def test_cli_module_import():
    """Test importing CLI module"""
    from src.cli import __all__
    assert __all__ == []

def test_cli_commands_module_import():
    """Test importing CLI commands module"""
    from src.cli.commands import __all__
    assert __all__ == []
