#!/usr/bin/env bash

if [[ $# -lt 1 ]]; then
  echo "Not enough arguments specified."
  echo "Usage:"
  echo "Bring up airflow, setup airflow connections/variables and authentication:  ./deploy.sh up"
  echo "Bring down airflow:                ./deploy.sh down"
  echo "Setup only airflow variables:      ./deploy.sh var"
  exit 0
fi

arg=${@:$OPTIND:1}

if [[ "$arg" = "up" ]]; then
  docker-compose -f docker-compose-${ENV}.yml $arg -d
  echo "Waiting 20s for airflow to come up before setting up airflow variables"
  sleep 20s
  path=/usr/local/airflow/src/airflow_dags/variables/variables.json
  docker exec dwc bash -l -c "airflow variables -i ${path}"
  echo "Setting up postgres connection in airflow"
  docker exec dwc bash -l -c "airflow connections --add --conn_id airflow_postgres --conn_type postgres --conn_host postgres --conn_login airflow --conn_password airflow --conn_schema airflow --conn_port 5432"
  echo "Setting up authentication"
  docker exec dwc bash -l -c "python /usr/local/airflow/src/settings/auth.py"
elif [[ "$arg" = "down" ]]; then
  docker-compose -f docker-compose-${ENV}.yml $arg
elif [[ "$arg" = "var" ]]; then
  path=/usr/local/airflow/src/airflow_dags/variables/variables.json
  docker exec dwc bash -l -c "airflow variables -i ${path}"
else
  echo "Invalid parameter specified"
  echo "Usage:"
  echo "Bring up airflow, setup airflow connections/variables and authentication:  ./deploy.sh up"
  echo "Bring down airflow:                ./deploy.sh down"
  echo "Setup only airflow variables:      ./deploy.sh var"
fi