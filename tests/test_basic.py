# -*- coding: utf-8 -*-
"""flaskcode module tests"""
from flask import url_for


def get_resource_data(client, file_name):
    return client.get(url_for('flaskcode.resource_data', file_path=file_name))


def test_index_endpoint(client):
    res = client.get(url_for('flaskcode.index'), follow_redirects=True)
    assert res.status_code == 200, 'test case for index_endpoint failed'


def test_resource_data_endpoint(client, file_name, file_content):
    res = get_resource_data(client, file_name)
    assert res.status_code == 200 and res.data == file_content.encode('utf-8'), 'test case for resource_data_endpoint failed'


def test_update_resource_data_endpoint(client, file_name, new_file_content):
    update_res = client.post(url_for('flaskcode.update_resource_data', file_path=file_name), data={
        'resource_data': new_file_content,
    })
    fetch_res = get_resource_data(client, file_name)
    assert update_res.status_code == 200 and update_res.json.get('success') == True and fetch_res.status_code == 200\
         and fetch_res.data == new_file_content.encode('utf-8'), 'test case for update_resource_data_endpoint failed'
