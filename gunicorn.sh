#!/bin/sh
gunicorn --pythonpath src/flask/ app:app -b 0.0.0.0:80