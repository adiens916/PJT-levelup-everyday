#!/bin/bash

function main {
  read -p "Do you want to create a new Django secret key and DB password?: [y/n] " ANSWER
  if [ $ANSWER == "y" ]; then
    create_secrets
  fi

  read -p "Do you want to assign urls for both frontend and backend?: [y/n] " ANSWER
  if [ $ANSWER == "y" ]; then
    assign_urls
  fi
}

function create_secrets {
  echo "< Django Secret Key >"
  echo "1. Open https://djecrety.ir/"
  echo "2. Generate a new Django Secret Key"
  read -p "3. Enter the key: " DJANGO_SECRET_KEY_INPUT
  env_replace DJANGO_SECRET_KEY $DJANGO_SECRET_KEY_INPUT .env

  echo "< DB Password >"
  read -p "Enter a new password for DB: " DB_PASSWORD_INPUT
  env_replace DJANGO_DB_PASSWORD $DB_PASSWORD_INPUT .env
}

function assign_urls {
  echo "< Backend Host >"
  read -p "Enter the backend host (Ex: www.your-domain.com): " BACKEND_HOST_INPUT
  env_replace BACKEND_HOST $BACKEND_HOST_INPUT .env

  echo "< Backend domain >"
  echo "Which scheme (protocol) is prefixed?"
  echo "1: http"
  echo "2: https"
  read -p "Enter: [1/2] " ANSWER
  if [ $ANSWER == "2" ]; then
    env_replace BACKEND_WITH_DOMAIN "https://${BACKEND_HOST_INPUT}" .env
    BACKEND_WITH_DOMAIN="https://${BACKEND_HOST_INPUT}"
  else
    env_replace BACKEND_WITH_DOMAIN "http://${BACKEND_HOST_INPUT}" .env
    BACKEND_WITH_DOMAIN="http://${BACKEND_HOST_INPUT}"
  fi
  echo "Your backend domain is ${BACKEND_WITH_DOMAIN}"

  echo "< Frontend Port >"
  read -p "Enter the port number used by frontend: " FRONTEND_PORT_INPUT
  env_replace FRONTEND_PORT ${FRONTEND_PORT_INPUT:-3000} .env

  echo "< Frontend Domain >"
  read -p "Does the frontend domain equals backend domain?: [y/n] " ANSWER
  if [ $ANSWER == "y" ]; then
    env_replace FRONTEND_WITH_DOMAIN $BACKEND_WITH_DOMAIN .env
  else
    read -p "Enter the domain used by frontend: " FRONTEND_WITH_DOMAIN_INPUT
    env_replace FRONTEND_WITH_DOMAIN $FRONTEND_WITH_DOMAIN_INPUT .env
  fi
}

function env_replace {
  key=$1
  val=$2
  filename=$3
  sed "s|${key}=.*|${key}=${val}|" -i $filename
}

main "$@"
