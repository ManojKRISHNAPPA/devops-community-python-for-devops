#!/bin/bash
yum install -y python3.12 -y
python3.12 -m venv pythonclass-py-3.12
python3 -m venv pythonclass-py-3.12
source pythonclass-py-3.12/bin/activate
pip3 install -r requirements.txt