"""flaskcode Flask Blueprint"""
import os

from flask import Blueprint, current_app, g, abort

from . import default_config
from ._version import __version__


__title__ = 'flaskcode'
__author__ = 'Sujeet Kumar'
__email__ = 'sujeetkv90@gmail.com'
__uri__ = 'https://github.com/sujeetkv/flaskcode'
__description__ = 'Web based code editor on python flask framework'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2019 Sujeet Kumar <sujeetkv90@gmail.com>'
__status__ = 'Development'


blueprint = Blueprint(
    'flaskcode',
    __name__,
    static_folder='static',
    template_folder='templates',
)


@blueprint.url_value_preprocessor
def manipulate_url_values(endpoint, values):
    if endpoint != 'flaskcode.static':
        resource_basepath = current_app.config.get('FLASKCODE_RESOURCE_BASEPATH')
        if not (resource_basepath and os.path.isdir(resource_basepath)):
            abort(500, '`FLASKCODE_RESOURCE_BASEPATH` is not a valid directory path')
        else:
            g.flaskcode_resource_basepath = os.path.abspath(resource_basepath).rstrip('/\\')


@blueprint.context_processor
def process_template_context():
    return dict(
        app_version=__version__,
        app_title=current_app.config.get('FLASKCODE_APP_TITLE', default_config.FLASKCODE_APP_TITLE),
        editor_theme=current_app.config.get('FLASKCODE_EDITOR_THEME', default_config.FLASKCODE_EDITOR_THEME),
    )


from . import views
