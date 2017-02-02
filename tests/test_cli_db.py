import pytest
from click.testing import CliRunner
from odoo_rpc_client_cli import cli

from .utils import get_connection_str


DB_NAME = 'rpc-client-cli-test-db'
UNEXISTING_DB_NAME = 'rpc-client-cli-test-db-unexisting-one-42'


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


def test_010_db_exists_false(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'exists', UNEXISTING_DB_NAME])
    assert result.exception
    assert result.exit_code != 0


def test_020_db_create(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'create', 'admin', DB_NAME])
    assert not result.exception
    assert result.exit_code == 0


def test_030_db_backup(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'backup', '--format', 'zip', 'admin', DB_NAME, 'test-backup-1'])
    assert not result.exception
    assert result.exit_code == 0


def test_040_db_drop(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'drop', 'admin', DB_NAME])
    assert not result.exception
    assert result.exit_code == 0


def test_050_db_restore(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'exists', DB_NAME])
    assert result.exception
    assert result.exit_code != 0, "DB must not exists here!"

    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'restore', 'admin', DB_NAME, 'test-backup-1'])
    assert not result.exception
    assert result.exit_code == 0


def test_060_db_drop(runner):
    result = runner.invoke(
        cli.main,
        ['--conn', get_connection_str(),
         'db', 'drop', 'admin', DB_NAME])
    assert not result.exception
    assert result.exit_code == 0
