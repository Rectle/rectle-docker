#!/bin/bash

cd src
# pipreqs .
# pip install -r requirements.txt

python -u code.py
# stdbuf -oL python code.py > log