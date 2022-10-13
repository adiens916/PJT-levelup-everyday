#!/bin/bash

backend_env="./backend/.env"
frontend_env="./frontend/.env"

function main {
  if test ! -f $backend_env; then
    add_template
  else
    load_env $backend_env
  fi
  update_env
}

function add_template {
  write $backend_env "# Should be changed"
  write $backend_env "## you can generate Django Secret Key from https://djecrety.ir/"
  write $backend_env "## or a random string by yourself."
  env_add $backend_env DJANGO_SECRET_KEY
  env_add $backend_env DJANGO_DB_PASSWORD

  write $backend_env ""
  write $backend_env "# Need to be changed when deploying"
  env_add $backend_env BACKEND_HOST
  env_add $backend_env BACKEND_WITH_DOMAIN
  env_add $backend_env FRONTEND_PORT 3000
  env_add $backend_env FRONTEND_WITH_DOMAIN
  
  write $backend_env ""
  write $backend_env "# Can be changed, depending on your situation."
  env_add $backend_env DJANGO_DB_ENGINE django.db.backends.mysql
  env_add $backend_env DJANGO_DB_USER root
  env_add $backend_env DJANGO_DB_NAME levelup_everyday_db
  env_add $backend_env DJANGO_DB_HOST localhost
  env_add $backend_env DJANGO_DB_PORT 3307

  env_add $frontend_env REACT_APP_BACKEND_HOST
}

function update_env {
  read -p "Do you want to update a new Django secret key and DB password?: [y/n] " ANSWER
  if test $ANSWER && [ $ANSWER == "y" ]; then
    create_django_secret_key
    create_db_password
  fi

  read -p "Do you want to assign urls for both frontend and backend?: [y/n] " ANSWER
  if test $ANSWER && [ $ANSWER == "y" ]; then
    create_backend_url
    create_frontend_url
  fi

  copy_backend_url_to_frontend
}

function create_django_secret_key {
  echo "< Django Secret Key >"
  echo "1. Open https://djecrety.ir/"
  echo "2. Generate a new Django Secret Key"
  read -p "3. Enter the key: " DJANGO_SECRET_KEY_INPUT
  env_replace $backend_env DJANGO_SECRET_KEY ${DJANGO_SECRET_KEY_INPUT:-DJANGO_SECRET_KEY}
}

function create_db_password {
  echo "< DB Password >"
  read -p "Enter a new password for DB: " DB_PASSWORD_INPUT
  env_replace $backend_env DJANGO_DB_PASSWORD ${DB_PASSWORD_INPUT:-DJANGO_DB_PASSWORD}
}

function create_backend_url {
  echo "< Backend Host>"
  read -p "Enter the backend host name: " BACKEND_HOST_INPUT
  env_replace $backend_env BACKEND_HOST ${BACKEND_HOST_INPUT:-BACKEND_HOST}

  if test ! $BACKEND_HOST_INPUT ; then
    BACKEND_WITH_DOMAIN=""
    env_replace $backend_env BACKEND_WITH_DOMAIN
    return
  fi

  echo "< Backend Protocol >"
  echo "Which scheme (protocol) is prefixed?"
  echo "1: http"
  echo "2: https"
  read -p "Enter: [1/2] " ANSWER
  if [ $ANSWER == "2" ]; then
    env_replace $backend_env BACKEND_WITH_DOMAIN "https://${BACKEND_HOST_INPUT}"
    BACKEND_WITH_DOMAIN="https://${BACKEND_HOST_INPUT}"
  else
    env_replace $backend_env BACKEND_WITH_DOMAIN "http://${BACKEND_HOST_INPUT}"
    BACKEND_WITH_DOMAIN="http://${BACKEND_HOST_INPUT}"
  fi
  echo "Your backend domain is ${BACKEND_WITH_DOMAIN}"
}

function create_frontend_url {
  echo "< Frontend Port >"
  read -p "Enter the port number used by frontend: " FRONTEND_PORT_INPUT
  env_replace $backend_env FRONTEND_PORT ${FRONTEND_PORT_INPUT:-3000} $FRONTEND_PORT

  echo "< Frontend Domain >"
  read -p "Does the frontend domain 'not' equal backend domain?: [y/n] " ANSWER

  if test $ANSWER && [ $ANSWER == "y" ]; then
    read -p "Enter the domain used by frontend: " FRONTEND_WITH_DOMAIN_INPUT
    env_replace $backend_env FRONTEND_WITH_DOMAIN ${FRONTEND_WITH_DOMAIN_INPUT:-FRONTEND_WITH_DOMAIN}
  else
    env_replace $backend_env FRONTEND_WITH_DOMAIN ${BACKEND_WITH_DOMAIN:-FRONTEND_WITH_DOMAIN}
  fi
}

function copy_backend_url_to_frontend {
  env_replace $frontend_env REACT_APP_BACKEND_HOST $BACKEND_WITH_DOMAIN $REACT_APP_BACKEND_HOST 
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

main "$@"
