import os
import click
from flask import Flask
from . import blueprint


def create_flask_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(blueprint)
    return app


@click.command()
@click.option('-h', '--host', default='127.0.0.1', help='IP or hostname on which to bind HTTP server')
@click.option('-p', '--port', default=5001, type=int, help='Port on which to bind HTTP server')
@click.option('-d', '--resource-basepath', default=None, help='Basepath for resources, default is current working directory')
@click.option('--debug/--normal', default=False, help='Enter DEBUG mode')
@click.option('--env', default='development', help='Flask environment, default is development')
@click.option('--app-title', default=None, help='Application title')
def run(host, port, resource_basepath, debug, env, app_title):
    click.echo('FlaskCode CLI')
    os.environ.setdefault('FLASK_ENV', env)
    os.environ.setdefault('FLASK_DEBUG', '1' if debug else '0')
    app = create_flask_app()
    app.config['FLASKCODE_RESOURCE_BASEPATH'] = resource_basepath or os.getcwd()
    app.config['FLASKCODE_APP_TITLE'] = app_title
    app.run(host=host, port=port, debug=debug)


def main():
    run(auto_envvar_prefix='FLASKCODE') # pylint:disable=unexpected-keyword-arg,no-value-for-parameter
