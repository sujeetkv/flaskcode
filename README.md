# flaskcode

[![Build Status](https://travis-ci.org/sujeetkv/flaskcode.svg?branch=master)](https://travis-ci.org/sujeetkv/flaskcode)
[![PyPI Version](https://img.shields.io/pypi/v/flaskcode.svg)](https://pypi.org/project/flaskcode)
[![MIT License](https://img.shields.io/github/license/sujeetkv/flaskcode.svg)](https://github.com/sujeetkv/flaskcode/blob/master/LICENSE)

Web based code editor on python flask framework.

![screenshot](https://user-images.githubusercontent.com/17122995/92307134-bc8f9e00-efb1-11ea-93c3-49aa6c52cca3.png)


## Installation

```bash
pip install flaskcode
```


## Run application from CLI

Run flaskcode standalone, using following command:

```bash
flaskcode /path/to/resource/folder
```

Get help for CLI command:

```bash
flaskcode --help
```

```
Usage: flaskcode [OPTIONS] [RESOURCE_BASEPATH]

  Run FlaskCode with given RESOURCE_BASEPATH or current working directory.

  All options can be set on the command line or through environment
  variables of the form FLASKCODE_*. For example FLASKCODE_USERNAME.

Options:
  -h, --host TEXT                 IP or hostname on which to run HTTP server.
  -p, --port INTEGER              Port on which to bind HTTP server.
  --username TEXT                 HTTP Basic Auth username.
  --password TEXT                 HTTP Basic Auth password.
  --editor-theme [vs|vs-dark|hc-black]
                                  Editor theme, default is vs-dark.
  --debug                         Run in flask DEBUG mode.
  --env TEXT                      Flask environment, default is development.
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```


## Integrating flaskcode in your Flask app

The flaskcode can be integrated in to your own `Flask` app by configuring and registering `flaskcode.blueprint` with your app:

```python
from flask import Flask
import flaskcode

app = Flask(__name__)
app.config.from_object(flaskcode.default_config)
app.config['FLASKCODE_RESOURCE_BASEPATH'] = '/path/to/resource/folder'
app.register_blueprint(flaskcode.blueprint, url_prefix='/flaskcode')

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
```

Now if you run the Flask app on default port, you can access the flaskcode at http://127.0.0.1:5000/flaskcode.


## Built with

* [Flask](http://flask.pocoo.org) - a python web framework
* [Monaco Editor](https://microsoft.github.io/monaco-editor) - a browser based code editor


## Authors

* [**Sujeet Kumar**](https://github.com/sujeetkv)


## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/sujeetkv/flaskcode/blob/master/LICENSE) file for details.
