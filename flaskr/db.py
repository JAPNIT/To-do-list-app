import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        """ g is a special function -- stores data that might be accessed by
        multiple functions during request -- saves the connection to the
        database"""

        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
            )

        """ current_app: represents the app without importing it """

        g.db.row_factory = sqlite3.Row

        return g.db

def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    """ open recource just opens the schema.sql relative to flaskr """
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

""" makes init_db runnable in the command line """
@click.command('init-db')
@with_appcontext

def init_db_command():
    """ clears the existing data and creates new tables """
    init_db()
    click.echo('Initialized the database. ')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


