import pytest
from click.testing import CliRunner
from odoo_rpc_client_cli import cli

from .utils import get_connection_str


@pytest.fixture
def runner():
    return CliRunner()


def test_001_db(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(), 'db']
    )
    assert result.exit_code == 0
    assert not result.exception
    # assert result.output.strip() == 'Hello, world.'


def test_010_db_exists_false(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'exists', 'rpc-client-cli-test-db-unexisting-one-42'])
    assert result.exception
    assert result.exit_code != 0


def test_020_db_create(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'create', 'admin', 'rpc-client-cli-test-db'])
    assert not result.exception
    assert result.exit_code == 0


def test_030_db_backup(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'backup', 'admin', 'rpc-client-cli-test-db', 'test-backup-1'])
    assert not result.exception
    assert result.exit_code == 0


def test_040_db_drop(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'drop', 'admin', 'rpc-client-cli-test-db'])
    assert not result.exception
    assert result.exit_code == 0


def test_050_db_restore(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'restore', 'admin', 'rpc-client-cli-test-db', 'test-backup-1'])
    assert not result.exception
    assert result.exit_code == 0


def test_060_db_drop(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'drop', 'admin', 'rpc-client-cli-test-db'])
    assert not result.exception
    assert result.exit_code == 0
