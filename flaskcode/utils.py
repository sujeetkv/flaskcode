# -*- coding: utf-8 -*-
import os
import io
import sys
import shutil
from functools import wraps
from flask import request, make_response


PY2 = sys.version_info.major == 2
DEFAULT_CHUNK_SIZE = 16 * 1024


if PY2:
    string_types = basestring # pylint:disable=undefined-variable
else:
    string_types = str


def get_file_extension(filename):
    # return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    ext = os.path.splitext(filename)[1]
    if ext.startswith('.'):
        ext = ext[1:]
    return ext.lower()


def write_file(content, filepath, encoding='utf-8', chunk_size=None):
    success = True
    message = 'File saved successfully'
    if isinstance(content, string_types):
        content_io = io.StringIO()
        content_io.write(content)
        with io.open(filepath, 'w', encoding=encoding, newline='\n') as dest:
            content_io.seek(0)
            try:
                shutil.copyfileobj(content_io, dest, chunk_size or DEFAULT_CHUNK_SIZE)
            except OSError as e:
                success = False
                message = 'Could not save file: ' + str(e)
    else:
        success = False
        message = 'Could not save file: Invalid content'
    return success, message


def dir_tree(abs_path, abs_root_path, exclude_names=None, excluded_extensions=None, allowed_extensions=None):
    tree = dict(
        name=os.path.basename(abs_path),
        path_name=abs_path[len(abs_root_path):].lstrip('/\\'),# TODO: use os.path.relpath
        children=[]
    )
    try:
        dir_entries = os.listdir(abs_path)
    except OSError:
        pass
    else:
        for name in dir_entries:
            if exclude_names and name in exclude_names:
                continue
            new_path = os.path.join(abs_path, name)
            if os.path.isdir(new_path):
                tree['children'].append(dir_tree(new_path, abs_root_path, exclude_names, excluded_extensions, allowed_extensions))
            else:
                ext = get_file_extension(name)
                if (excluded_extensions and ext in excluded_extensions) or (allowed_extensions and ext not in allowed_extensions):
                    continue
                tree['children'].append(dict(
                    name=os.path.basename(new_path),
                    path_name=new_path[len(abs_root_path):].lstrip('/\\'),# TODO: use os.path.relpath
                    is_file=True,
                ))
    return tree


def head_compatible(route_handler):
    """View decorator to make view handler compatible for `HEAD` method request."""
    @wraps(route_handler)
    def decorated_function(*args, **kwargs):
        if request.method == 'HEAD':
            route_response = route_handler(*args, **kwargs)
            response = make_response()
            response.headers.clear()
            response.headers.extend(route_response.headers)
            return response
        else:
            return route_handler(*args, **kwargs)
    return decorated_function
