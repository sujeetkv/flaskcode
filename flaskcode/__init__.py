# -*- coding: utf-8 -*-
"""flaskcode Flask Blueprint"""
import os
from flask import Blueprint, current_app, g, abort
from . import __pkginfo__, default_config


__title__ = __pkginfo__.title
__version__ = __pkginfo__.version
__author__ = __pkginfo__.author
__email__ = __pkginfo__.email
__uri__ = __pkginfo__.uri
__description__ = __pkginfo__.description
__license__ = __pkginfo__.license
__copyright__ = __pkginfo__.copyright
__status__ = __pkginfo__.status


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
