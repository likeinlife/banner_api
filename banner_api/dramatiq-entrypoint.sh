#!/bin/sh

delay=1
while true; do

  if [ "$APP_DEBUG" = "True" ]; then
      echo "DEBUG MODE"
      dramatiq actors.setup --watch .
  else
      echo "RELEASE MODE"
      dramatiq actors.setup
  fi
  if [ $? -eq 3 ]; then
    echo "Connection error encountered on startup. Retrying in $delay second(s)..."
    sleep $delay
    delay=$((delay * 2))
  else
    exit $?
  fi
done