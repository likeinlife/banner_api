#!/bin/sh

delay=1
while true; do
  dramatiq actors.setup --watch .
  if [ $? -eq 3 ]; then
    echo "Connection error encountered on startup. Retrying in $delay second(s)..."
    sleep $delay
    delay=$((delay * 2))
  else
    exit $?
  fi
done