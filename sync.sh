#!/bin/bash

function main {
  create_db_env
  create_backend_env_from_db
  create_frontend_env_from_backend
}

function create_db_env {
  echo 
}

function create_backend_env_from_db {
  BACKEND_URL='example.com'
}

function create_frontend_env_from_backend {
  source frontend/create_env.sh ${BACKEND_URL}
}

main "$@"
