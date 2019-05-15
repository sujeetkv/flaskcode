# -*- coding: utf-8 -*-
"""flaskcode cli module"""

import os
import click
from flask import Flask
from . import blueprint, default_config


def create_flask_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(blueprint)
    return app


@click.command(help='Run %s with given RESOURCE_BASEPATH or current working directory.' % default_config.FLASKCODE_APP_TITLE)
@click.argument('resource-basepath', default=os.getcwd(), type=os.path.abspath, required=False)
@click.option('-h', '--host', default='127.0.0.1', help='IP or hostname on which to bind HTTP server')
@click.option('-p', '--port', default=5001, type=int, help='Port on which to bind HTTP server')
@click.option('--debug/--normal', default=False, help='Enter DEBUG mode')
@click.option('--env', default='development', help='Flask environment, default is development')
def run(resource_basepath, host, port, debug, env):
    os.environ.setdefault('FLASK_ENV', env)
    os.environ.setdefault('FLASK_DEBUG', '1' if debug else '0')
    click.echo('%s CLI: %s' % (default_config.FLASKCODE_APP_TITLE, resource_basepath))
    click.echo('')
    app = create_flask_app()
    app.config['FLASKCODE_RESOURCE_BASEPATH'] = resource_basepath
    app.run(host=host, port=port, debug=debug)


def main():
    run(auto_envvar_prefix='FLASKCODE') # pylint:disable=unexpected-keyword-arg,no-value-for-parameter
