#!/bin/bash

fswatch -0 ./api.py | while read -d "" event
  do
    echo "Rebuild and restart hodor-server"
    docker rm -f hodor-server-container
    docker build -t hodor-server . && docker run --rm --name hodor-server-container -p 8080:8080 hodor-server &
  done