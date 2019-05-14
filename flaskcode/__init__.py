import os
from flask import Blueprint, current_app, g, abort
from . import default_config


blueprint = Blueprint(
    'flaskcode',
    __name__,
    static_folder='static',
    template_folder='templates',
)


@blueprint.url_value_preprocessor
def manipulate_url_values(endpoint, values):
    if endpoint != 'flaskcode.static':
        resource_basepath = current_app.config.get('FLASKCODE_RESOURCE_BASEPATH', default_config.FLASKCODE_RESOURCE_BASEPATH)
        if not (resource_basepath and os.path.isdir(resource_basepath)):
            abort(500, '`FLASKCODE_RESOURCE_BASEPATH` is not a valid directory path')
        else:
            g.flaskcode_resource_basepath = os.path.abspath(resource_basepath).rstrip('/\\')


@blueprint.context_processor
def process_template_context():
    return dict(
        app_title=current_app.config.get('FLASKCODE_APP_TITLE') or default_config.FLASKCODE_APP_TITLE,
    )


from . import views
