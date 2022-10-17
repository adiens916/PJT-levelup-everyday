#!/bin/bash

function main {
  create_db_env
  create_backend_env_from_db
  create_frontend_env_from_backend
}

function create_db_env {
  source create_db.sh
}

function create_backend_env_from_db {
  source .env
  source backend/create_env.sh ${MYSQL_ROOT_PASSWORD}
}

function create_frontend_env_from_backend {
  source frontend/create_env.sh ${BACKEND_URL}
}

main "$@"
