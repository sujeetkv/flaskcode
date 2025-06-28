"""flaskcode cli module"""
import os
import sys

import click
from flask import Flask, request, make_response

from . import blueprint, default_config, __title__, __version__


help_str = """Run {app_title} with given RESOURCE_BASEPATH or current working directory.

All options can be set on the command line or through environment
variables of the form FLASKCODE_*. For example FLASKCODE_USERNAME.
""".format(app_title=default_config.FLASKCODE_APP_TITLE)


themes = ['vs', 'vs-dark', 'hc-black']


def add_auth(blueprint, username, password, realm=default_config.FLASKCODE_APP_TITLE):
    @blueprint.before_request
    def http_basic_auth():
        auth = request.authorization
        if not (auth and auth.password == password and auth.username == username):
            response = make_response('Unauthorized', 401)
            response.headers.set('WWW-Authenticate', 'Basic realm="%s"' % realm)
            return response
        return None


def create_flask_app(username=None, password=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(default_config)
    if username:
        add_auth(blueprint, username, password)
    app.register_blueprint(blueprint)
    return app


@click.command(help=help_str)
@click.argument('resource-basepath', default=os.getcwd(), type=os.path.abspath, required=False)
@click.option('-h', '--host', default='127.0.0.1', help='IP or hostname on which to run HTTP server.')
@click.option('-p', '--port', default=5001, type=int, help='Port on which to bind HTTP server.')
@click.option('--username', default=None, help='HTTP Basic Auth username.')
@click.option('--password', default=None, help='HTTP Basic Auth password.')
@click.option('--editor-theme', default='vs-dark', type=click.Choice(themes), help='Editor theme, default is vs-dark.')
@click.option('--debug', default=False, is_flag=True, help='Run in flask DEBUG mode.')
@click.option('--env', default='development', help='Flask environment, default is development.')
@click.version_option(version=__version__, prog_name=__title__)
def run(resource_basepath, host, port, username, password, editor_theme, debug, env):
    os.environ.setdefault('FLASK_ENV', env)
    os.environ.setdefault('FLASK_DEBUG', '1' if debug else '0')
    click.echo('%s CLI: %s' % (default_config.FLASKCODE_APP_TITLE, resource_basepath))
    click.echo('')
    app = create_flask_app(username=username, password=password)
    app.config['FLASKCODE_RESOURCE_BASEPATH'] = resource_basepath
    app.config['FLASKCODE_EDITOR_THEME'] = editor_theme
    app.run(host=host, port=port, debug=debug)


def main():
    try:
        run(auto_envvar_prefix='FLASKCODE') # pylint:disable=unexpected-keyword-arg,no-value-for-parameter
    except KeyboardInterrupt:
        sys.stderr.write('\n')
        return 1
    except Exception as err:
        sys.stderr.write('Error: %s\n' % err)
        return 1
    return 0
