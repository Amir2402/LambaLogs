#!/usr/bin/bash

source ~/dirs/myenv/bin/activate #path to virtual env

export SUPERSET_SECRET_KEY=Test1212-
export FLASK_APP=superset

superset db upgrade 
superset init
superset run -p 8088 --with-threads --reload --debugger