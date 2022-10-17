#!/bin/bash

env_file=".env"


function main {
  init_backend_env

  create_django_secret_key
  
  DB_PASSWORD=$1
  add_db_password $DB_PASSWORD

  add_backend_url
  add_frontend_url
}

function init_backend_env {
  set_absolute_path

  if test -f ${env_file}; then
    load_env ${env_file}
    return 
  fi

  write ${env_file} "# Should be changed"
  write ${env_file} "## you can generate Django Secret Key from https://djecrety.ir/"
  write ${env_file} "## or a random string by yourself."
  env_add ${env_file} DJANGO_SECRET_KEY
  env_add ${env_file} DJANGO_DB_PASSWORD

  write ${env_file} ""
  write ${env_file} "# Need to be changed when deploying"
  env_add ${env_file} BACKEND_HOST
  env_add ${env_file} BACKEND_WITH_DOMAIN
  env_add ${env_file} FRONTEND_PORT 3000
  env_add ${env_file} FRONTEND_WITH_DOMAIN
  
  write ${env_file} ""
  write ${env_file} "# Can be changed, depending on your situation."
  env_add ${env_file} DJANGO_DB_ENGINE django.db.backends.mysql
  env_add ${env_file} DJANGO_DB_USER root
  env_add ${env_file} DJANGO_DB_NAME levelup_everyday_db
  env_add ${env_file} DJANGO_DB_HOST localhost
  env_add ${env_file} DJANGO_DB_PORT 3307
}

function create_django_secret_key {
  if test -f ${env_file}; then
    echo
    read -p "New Django secret key? [y/n]: " ANSWER

    if test ! $ANSWER || [ $ANSWER != "y" ]; then
      return
    fi
  fi

  echo
  echo "1. Open https://djecrety.ir/"
  echo "2. Generate a new Django Secret Key"
  echo "3. Enter the key"
  echo
  read -p ": " DJANGO_SECRET_KEY_INPUT
  env_replace ${env_file} DJANGO_SECRET_KEY ${DJANGO_SECRET_KEY_INPUT:-${DJANGO_SECRET_KEY}}
}

function add_db_password {
  DB_PASSWORD=$1
  if test ${DB_PASSWORD}; then
    env_replace ${env_file} DJANGO_DB_PASSWORD ${DB_PASSWORD:-${DJANGO_DB_PASSWORD}}
    return
  fi
  
  if test -f ${env_file}; then
    echo
    read -p "New DB password? [y/n]: " ANSWER

    if test ! $ANSWER || [ $ANSWER != "y" ]; then
      return
    fi
  fi

  echo
  echo "Enter a new password for DB" 
  echo
  read -p ": " DB_PASSWORD_INPUT
  env_replace ${env_file} DJANGO_DB_PASSWORD ${DB_PASSWORD_INPUT:-${DJANGO_DB_PASSWORD}}
}

function add_backend_url {
  if test -f ${env_file}; then
    echo
    read -p "New backend URL? [y/n]: " ANSWER

    if test ! $ANSWER || [ $ANSWER != "y" ]; then
      return
    fi
  fi

  echo
  echo "Enter full backend URL (Ex. https://www.example.com/api)"
  echo
  read -p ": " BACKEND_URL

  WITHOUT_PROTOCOL=$(echo ${BACKEND_URL#http?://})
  WITHOUT_PATH=$(echo ${WITHOUT_PROTOCOL} | cut -d "/" -f1)
  BACKEND_HOST=${WITHOUT_PATH}
  BACKEND_WITH_DOMAIN=${BACKEND_URL}

  env_replace ${env_file} BACKEND_HOST ${BACKEND_HOST}
  env_replace ${env_file} BACKEND_WITH_DOMAIN ${BACKEND_WITH_DOMAIN}
}

function add_frontend_url {
  if test -f ${env_file}; then
    echo
    read -p "New frontend URL? [y/n]: " ANSWER

    if test ! $ANSWER || [ $ANSWER != "y" ]; then
      return
    fi
  fi

  echo
  read -p "Does frontend URL *NOT* equal backend URL?: [y/n] " ANSWER

  if test $ANSWER && [ $ANSWER == "y" ]; then
    echo
    echo "Enter frontend URL (Ex. http://www.frontend.com)"
    echo
    read -p ": " FRONTEND_WITH_DOMAIN_INPUT
    env_replace ${env_file} FRONTEND_WITH_DOMAIN ${FRONTEND_WITH_DOMAIN_INPUT}
  else
    env_replace ${env_file} FRONTEND_WITH_DOMAIN ${BACKEND_WITH_DOMAIN}
  fi
}

function set_absolute_path {
  RELATIVE_PATH=$(dirname $BASH_SOURCE)
  ABSOLUTE_PATH=$(readlink -f $RELATIVE_PATH)
  env_file=${ABSOLUTE_PATH}/${env_file}
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

function load_env {
  filename=$1
  if test -f $filename; then
    set -a; source $filename; set +a
  fi
}

function write {
  filename=$1
  contents=$2

  echo $contents >> $filename
}

main $@
