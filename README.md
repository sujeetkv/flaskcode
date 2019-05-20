# flaskcode
Web based code editor for flask

[![Build Status](https://travis-ci.org/sujeetkv/flaskcode.svg?branch=master)](https://travis-ci.org/sujeetkv/flaskcode)


## Installation

```bash
$ pip install flaskcode
```


## Running the application

Run the application standalone, like this:

```bash
$ flaskcode /path/to/resource/folder
FlaskCode CLI: /path/to/resource/folder
...
```

```bash
$ flaskcode --help
Usage: flaskcode [OPTIONS] [RESOURCE_BASEPATH]

  Run FlaskCode with given RESOURCE_BASEPATH or current working directory.

Options:
  -h, --host TEXT     IP or hostname on which to bind HTTP server
  -p, --port INTEGER  Port on which to bind HTTP server
  --debug / --normal  Enter DEBUG mode
  --env TEXT          Flask environment, default is development
  --help              Show this message and exit.
```


## Integrating flaskcode in your Flask app

The flaskcode can be integrated in to your own `Flask` app by accessing the blueprint directly in the normal way, e.g.:

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

If you start the Flask app on the default port, you can access the flaskcode at http://localhost:5000/flaskcode.
