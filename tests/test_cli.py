from click.testing import CliRunner
from body_tracking.cli import main


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Run the body tracking CLI" in result.output
