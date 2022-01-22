#!/bin/bash -l
if [ "${ENVIRONMENT}" != "" ] && [ "${ENVIRONMENT}" == "local" ]
  then
    tail -f /dev/null
fi
python src/main.py
