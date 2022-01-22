#!/bin/bash -l
if [ "${ENVIRONMENT}" != "" ] && [ "${ENVIRONMENT}" == "local" ]
  then
    tail -f /dev/null
fi
exec python src/utils.py &
exec streamlit run src/app.py
