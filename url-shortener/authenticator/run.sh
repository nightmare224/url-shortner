#!/bin/bash

ABSPATH=`readlink -f $0`
DIRPATH=`dirname $ABSPATH`
cd ${DIRPATH}

gunicorn -c gunicorn.conf.py app:app