# -*- coding: utf-8 -*-

import pytest
from flaskcode.cli import create_flask_app


@pytest.fixture
def app(request):
    application = create_flask_app()
    #application.config['TESTING'] = True
    application.testing = True
    with application.app_context():
        yield application


@pytest.fixture
def client(request, app):
    client = app.test_client()
    def teardown():
        pass
    request.addfinalizer(teardown)
    return client


@pytest.fixture
def resource_dir(tmp_path):
    return tmp_path / 'src'


@pytest.fixture
def resource_file(resource_dir):
    resource_file_path = resource_dir / 'script.js'
    resource_file_path.write_text('var x = 5;')
    return resource_file_path


def pytest_report_header(config):
    return '***** Tests for flaskcode package *****'
