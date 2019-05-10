import os
from flask import Blueprint, current_app, g, abort


blueprint = Blueprint(
    'flaskcode',
    __name__,
    url_prefix='/flaskcode',
    static_folder='static',
    template_folder='templates',
)


@blueprint.url_value_preprocessor
def manipulate_url_values(endpoint, values):
    if endpoint != 'flaskcode.static':
        resource_dir = values['resource_dir']
        default_path = os.path.join(current_app.root_path, 'resources')
        g.resource_basepath = current_app.config.get('FLASKCODE_RESOURCE_BASEPATH', default_path).rstrip('/\\')
        g.resource_dir_path = os.path.join(g.resource_basepath, resource_dir)
        if not os.path.isdir(g.resource_dir_path):
            abort(404)


@blueprint.context_processor
def process_template_context():
    return dict(
        app_title='FlaskCode',
    )


from . import views
