
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
virtualenv ivenv
source ivenv/bin/activate
pip install -r requirements.txt

export FLASK_APP=img_compressor.py
export FLASK_ENV=development
flask run
