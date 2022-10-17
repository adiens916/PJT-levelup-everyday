#!/bin/bash

env_file=".env"

function main {
  if test ! -f ${env_file}; then
    set_absolute_path
    create_db_password
    add_db_name_and_port
  fi
}

function create_db_password {
  echo "Write DB password"
  read -p ": " DB_PASSWORD_INPUT
  env_add ${env_file} MYSQL_ROOT_PASSWORD ${DB_PASSWORD_INPUT}
}

function add_db_name_and_port {
  env_add ${env_file} MYSQL_DATABASE levelup_everyday_db
  env_add ${env_file} MYSQL_PORT 3307
}

function set_absolute_path {
  # https://codechacha.com/ko/how-to-get-path-of-bash-script/#readlink으로-파일-경로-얻기-1
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

main $@
