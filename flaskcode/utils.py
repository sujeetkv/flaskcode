import os
import io
import shutil


DEFAULT_CHUNK_SIZE = 16 * 1024


def get_file_extension(filename):
    # return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    ext = os.path.splitext(filename)[1]
    if ext.startswith('.'):
        ext = ext[1:]
    return ext.lower()


def write_file(content, filepath, encoding='utf-8', newline='\n', chunk_size=None):
    success = True
    message = 'File saved successfully'
    if isinstance(content, str):
        content_buffer = io.StringIO(content, newline=newline)
        with io.open(filepath, 'w', encoding=encoding, newline=newline) as dest:
            content_buffer.seek(0)
            try:
                shutil.copyfileobj(content_buffer, dest, chunk_size or DEFAULT_CHUNK_SIZE)
            except OSError as err:
                success = False
                message = 'Could not save file: ' + str(err)
    else:
        success = False
        message = 'Could not save file: Invalid content'
    return success, message


def dir_tree(abs_path, abs_root_path, exclude_names=None, excluded_extensions=None, allowed_extensions=None):
    tree = dict(
        name=os.path.basename(abs_path),
        path_name=os.path.relpath(abs_path, abs_root_path).replace('\\', '/').lstrip('/'),
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
                tree['children'].append(
                    dir_tree(new_path, abs_root_path, exclude_names, excluded_extensions, allowed_extensions)
                )
            else:
                ext = get_file_extension(name)
                if (
                    (excluded_extensions and ext in excluded_extensions) or
                    (allowed_extensions and ext not in allowed_extensions)
                ):
                    continue
                tree['children'].append(dict(
                    name=os.path.basename(new_path),
                    path_name=os.path.relpath(new_path, abs_root_path).replace('\\', '/').lstrip('/'),
                    is_file=True,
                ))
    return tree
