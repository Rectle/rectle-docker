#!/bin/bash

if [ "$DEBUG" = "true" ]; then
    sleep infinity
else
    python -u src/main.py
fi