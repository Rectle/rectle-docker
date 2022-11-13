#!/bin/bash

cd src
pipreqs .
pip install -r requirements.txt

python test.py > result.log 2> error.log