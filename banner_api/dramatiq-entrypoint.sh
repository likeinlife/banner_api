#!/bin/sh

delay=1
while true; do

  if [ "$APP_DEBUG" = "True" ]; then
      dramatiq actors.setup --watch .
      echo "DEBUG MODE"
  else
      dramatiq actors.setup
      echo "RELEASE MODE"
  fi
  if [ $? -eq 3 ]; then
    echo "Connection error encountered on startup. Retrying in $delay second(s)..."
    sleep $delay
    delay=$((delay * 2))
  else
    exit $?
  fi
done