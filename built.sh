
#!/usr/bin/env bash
# exit on error
set -o errexit

virtualenv ivenv
source ivenv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip
