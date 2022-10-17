#!/bin/bash

frontend_env=".env.production"

function main {
  set_absolute_path
  create_frontend_env
  
  BACKEND_URL=$1
  if test ! ${BACKEND_URL}; then
    update_frontend_env
  else
    sync_frontend_env
  fi
}

function set_absolute_path {
  # https://codechacha.com/ko/how-to-get-path-of-bash-script/#readlink으로-파일-경로-얻기-1
  RELATIVE_PATH=$(dirname $BASH_SOURCE)
  ABSOLUTE_PATH=$(readlink -f $RELATIVE_PATH)
  frontend_env=${ABSOLUTE_PATH}/${frontend_env}
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
