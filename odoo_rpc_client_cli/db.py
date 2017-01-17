import click
import sys

from . cli import main


@main.group()
@click.pass_context
def db(ctx):
    """ Manage server databases
    """
    pass


@db.command()
@click.pass_context
def list(ctx):
    """ List databases available on server
    """
    cl = ctx.obj['client']
    for db in cl.services.db.list_db():
        click.echo(db)


@db.command()
@click.argument('dbname', required=True)
@click.pass_context
def exists(ctx, dbname):
    """ Test if database 'dbname' exists
    """
    if ctx.obj['client'].services.db.db_exist(dbname):
        click.echo("DB '%s' exists!" % dbname)
    else:
        click.echo("DB '%s' does not exists!" % dbname)
        sys.exit(1)  # non-zero status code for to be useful by external tools


@db.command()
@click.argument('password', required=True)
@click.argument('dbname', required=True)
@click.option('--demo', is_flag=True, default=False, help="Load demo data?")
@click.option('--lang', default='en_US', help="What language to use")
@click.option('--admin-password', default='admin',
              help="Password for auto-created admin user")
@click.pass_context
def create(ctx, password, dbname, demo, lang, admin_password):
    """ Create database
    """
    ctx.obj['client'].services.db.create_database(
        password, dbname, demo, lang, admin_password)


@db.command()
@click.argument('password', required=True)
@click.argument('dbname', required=True)
@click.pass_context
def drop(ctx, password, dbname):
    """ Drop database
    """
    ctx.obj['client'].services.db.drop_db(password, dbname)


@db.command()
@click.argument('password', required=True)
@click.argument('dbname', required=True)
@click.argument('file', required=True, type=click.File(mode='wb'))
@click.option('--format', default="sql", type=click.Choice(['sql', 'zip']),
              show_default=True,
              help="Backup format. "
                   "Note: 'zip' format supported only by odoo 8.0+")
@click.pass_context
def backup(ctx, password, dbname, file, format):
    """ Backup database to file
    """
    import base64
    dump_data = ctx.obj['client'].services.db.dump_db(password, dbname,
                                                      format=format)
    file.write(base64.b64decode(dump_data))


@db.command()
@click.argument('password', required=True)
@click.argument('dbname', required=True)
@click.argument('file', required=True, type=click.File(mode='rb'))
@click.option('--is-copy', default=False, is_flag=True,
              help="Restore database as copy?")
@click.pass_context
def restore(ctx, password, dbname, file, is_copy):
    """ Restore database
    """
    import base64
    data = file.read()
    ctx.obj['client'].services.db.restore_db(password, dbname,
                                             base64.b64encode(data),
                                             copy=is_copy)
