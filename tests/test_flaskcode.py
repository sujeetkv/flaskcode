# -*- coding: utf-8 -*-
"""flaskcode module tests"""
from flask import url_for


# helpers
def get_resource_data(client, file_name):
    return client.get(url_for('flaskcode.resource_data', file_path=file_name))


# tests
def test_index_endpoint(client):
    res = client.get(url_for('flaskcode.index'), follow_redirects=True)
    assert res.status_code == 200, 'index_endpoint access failed'


def test_resource_data_endpoint(client, file_name, file_content, file_name_404):
    res = get_resource_data(client, file_name)
    res404 = get_resource_data(client, file_name_404)
    assert res.status_code == 200 and res.data == file_content.encode('utf-8'), 'existing resource_data_endpoint test failed'
    assert res404.status_code == 404, 'non existing resource_data_endpoint test failed'


def test_update_resource_data_endpoint(client, file_name, file_content_update, new_file_name, new_file_content):
    update_res = client.post(url_for('flaskcode.update_resource_data', file_path=file_name), data={
        'resource_data': file_content_update,
    })
    updated_res = get_resource_data(client, file_name)

    create_res = client.post(url_for('flaskcode.update_resource_data', file_path=new_file_name), data={
        'resource_data': new_file_content,
        'is_new_resource': 1,
    })
    created_res = get_resource_data(client, new_file_name)

    assert update_res.status_code == 200 and update_res.json.get('success') == True and updated_res.status_code == 200\
         and updated_res.data == file_content_update.encode('utf-8'), 'update_resource_data_endpoint for update test failed'
    assert create_res.status_code == 200 and create_res.json.get('success') == True and created_res.status_code == 200\
         and created_res.data == new_file_content.encode('utf-8'), 'update_resource_data_endpoint for create test failed'
