#!/bin/bash

if [ ! -d "env" ]; then
    virtualenv env
    ./env/bin/pip install wfdb
    echo 'Execute the above line to enable the virtualenv'
    echo 'source ./env/bin/activate'
else
    echo "directory env already exists"
fi
