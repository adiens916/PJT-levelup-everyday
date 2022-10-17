#!/bin/bash

frontend_env="./.env.production"
BACKEND_URL=$1

function main {
  create_frontend_env
  if test ! ${BACKEND_URL}; then
    update_frontend_env
  else
    sync_frontend_env
  fi
}

function create_frontend_env {
  if test ! -f ${frontend_env}; then
    env_add ${frontend_env} REACT_APP_BACKEND_HOST
  fi
}

function update_frontend_env {
  echo "Write URL to backend API (Ex. https://www.example.com/api)"
  read -p ": " BACKEND_URL_INPUT
  env_replace ${frontend_env} REACT_APP_BACKEND_HOST ${BACKEND_URL_INPUT}
}

function sync_frontend_env {
  env_replace ${frontend_env} REACT_APP_BACKEND_HOST ${BACKEND_URL}
}

function env_add {
  filename=$1
  key=$2
  val=$3
  echo "${key}=${val}" >> $filename
}

function env_replace {
  filename=$1
  key=$2
  val=$3
  sed "s|${key}=.*|${key}=${val}|" -i $filename
}

main $@
