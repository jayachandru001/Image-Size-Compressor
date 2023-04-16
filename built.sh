
#!/usr/bin/env bash
# exit on error
set -o errexit

virtualenv ivenv
source ivenv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip

export FLASK_APP = img_compressor.py
export FLASK_ENV = development
export flask run
