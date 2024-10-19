#! /bin/bash

cd "$(dirname -- "$(readlink -f -- "$0";)";)";
sudo docker compose up --build --force-recreate