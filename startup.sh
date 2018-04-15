#!/bin/bash

# this script presumes you have installed a VirtualEnv in 'venv' and 
# run 'pip install -r requirements'.
#
source venv/bin/activate
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run
