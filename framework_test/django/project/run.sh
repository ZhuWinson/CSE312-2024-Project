#! /bin/bash

cd "$(dirname -- "$(readlink -f -- "$0";)";)";
python3 manage.py runserver
