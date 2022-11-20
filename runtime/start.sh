#!/bin/bash

cp -r storage src
cd src
pipreqs .
pip install -r requirements.txt

python -u main.py
# stdbuf -oL python code.py > log