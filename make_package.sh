#!/bin/bash -x

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

cd venv/lib/python3.9/site-packages
zip -r ../../../../lambda_package.zip .
cd ../../../../

zip -r lambda_package.zip\
    app\
    lambda_function.py

echo "Finished make_package.sh"
