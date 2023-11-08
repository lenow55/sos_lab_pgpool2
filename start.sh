#!/bin/bash

sudo -v
if [[ $1 = "dev" ]]
then
    sudo docker-compose -f docker-compose.yml -f docker-compose.development.yml up --build
fi
if [[ $1 = "build" ]]
then
    sudo docker-compose -f docker-compose.yml up --build
fi

