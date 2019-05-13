import os
import click
from flask import Flask
from flask.cli import load_dotenv
from . import blueprint


def create_flask_app(url_prefix=None):
    load_dotenv()
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(blueprint, url_prefix=url_prefix)
    return app


@click.command()
@click.option('-h', '--host', default='0.0.0.0', help='IP or hostname on which to bind HTTP server')
@click.option('-p', '--port', default=5001, type=int, help='Port on which to bind HTTP server')
@click.option('--url-prefix', default=None, help='URL prefix e.g. for use behind a reverse proxy')
@click.option('--debug', default=False, help='Enter DEBUG mode')
def run(host, port, url_prefix, debug):
    click.echo('FlaskCode')
    app = create_flask_app(url_prefix)
    app.config['FLASKCODE_RESOURCE_BASEPATH'] = os.getcwd()
    app.run(host=host, port=port, debug=debug)


def main():
    run(auto_envvar_prefix='FLASKCODE') # pylint:disable=unexpected-keyword-arg,no-value-for-parameter
