import pytest
from click.testing import CliRunner
from odoo_rpc_client_cli import cli

from .utils import get_connection_str


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception
    # assert result.output.strip() == 'Hello, world.'


def test_cli_with_option(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str()])
    assert result.exception
    assert result.exit_code != 0  # missing command


def test_cli_with_empty_option(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', ''])
    assert result.exception
    assert result.exit_code != 0


def test_cli_with_bad_option(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', 'some-unacceptable-option'])
    assert result.exception
    assert result.exit_code != 0
