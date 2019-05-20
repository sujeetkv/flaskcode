# -*- coding: utf-8 -*-
import pytest
from flaskcode.cli import create_flask_app


FILE_NAME = 'script.js'
FILE_NAME_404 = 'nonexistingfile.txt'
FILE_CONTENT = b'var x = 5;'.decode('utf-8')
FILE_CONTENT_UPDATE = b'var x = 10;'.decode('utf-8')
NEW_FILE_NAME = 'testfile.txt'
NEW_FILE_CONTENT = b'This is test content.'.decode('utf-8')


def pytest_report_header(config):
    return 'Running tests for flaskcode package...'


@pytest.fixture
def file_name():
    return FILE_NAME


@pytest.fixture
def file_name_404():
    return FILE_NAME_404


@pytest.fixture
def file_content():
    return FILE_CONTENT


@pytest.fixture
def file_content_update():
    return FILE_CONTENT_UPDATE


@pytest.fixture
def new_file_name():
    return NEW_FILE_NAME


@pytest.fixture
def new_file_content():
    return NEW_FILE_CONTENT


@pytest.fixture
def resource_dir(tmp_path, file_name, file_content):
    resource_dir_path = tmp_path / 'src'
    resource_dir_path.mkdir()
    (resource_dir_path / file_name).write_text(file_content)
    return resource_dir_path


@pytest.fixture
def app(request, resource_dir):
    application = create_flask_app()
    #application.config['TESTING'] = True
    application.testing = True
    application.config['SERVER_NAME'] = '127.0.0.1:5000'
    application.config['FLASKCODE_RESOURCE_BASEPATH'] = str(resource_dir)
    with application.app_context():
        yield application


@pytest.fixture
def client(request, app):
    client = app.test_client()
    def teardown():
        pass
    request.addfinalizer(teardown)
    return client
