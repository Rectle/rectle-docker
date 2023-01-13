#!/bin/bash
cd storage
python cloud_storage_controller.py

cd ..
pipreqs .
pip install -r requirements.txt

cd src
python -u code.py
# stdbuf -oL python code.py > log