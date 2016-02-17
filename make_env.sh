#!/bin/sh
virtualenv --distribute V_ENV --no-site-packages
source V_ENV_TMP/bin/activate
pip install tornado==4.2
pip install anyjson==0.3.3
pip install toamqp
python setup.py develop

