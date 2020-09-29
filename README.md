# docker-airflow
[![CircleCI](https://circleci.com/gh/puckel/docker-airflow/tree/master.svg?style=svg)](https://circleci.com/gh/puckel/docker-airflow/tree/master)
[![Docker Build Status](https://img.shields.io/docker/build/puckel/docker-airflow.svg)]()

[![Docker Hub](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/r/puckel/docker-airflow/)
[![Docker Pulls](https://img.shields.io/docker/pulls/puckel/docker-airflow.svg)]()
[![Docker Stars](https://img.shields.io/docker/stars/puckel/docker-airflow.svg)]()

This repository contains **Dockerfile** of [apache-airflow](https://github.com/apache/incubator-airflow) for [Docker](https://www.docker.com/)'s [automated build](https://registry.hub.docker.com/u/puckel/docker-airflow/) published to the public [Docker Hub Registry](https://registry.hub.docker.com/).

## Informations

* Based on Python (3.6-slim) official Image [python:3.6-slim](https://hub.docker.com/_/python/) and uses the official [Postgres](https://hub.docker.com/_/postgres/) as backend and [Redis](https://hub.docker.com/_/redis/) as queue
* Install [Docker](https://www.docker.com/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)
* Following the Airflow release from [Python Package Index](https://pypi.python.org/pypi/apache-airflow)

## Environment 
Following env variable is required on the host for docker-ariflow

    export ENV=<dev|tst|lt2|prd>

NB: Also please make sure the HOST bash_profile has PATH set as container will inherit from it.


## Project btb specific 
Following directories need to exists with read and write permission as the current user (e.g. maprsouth) for btb.
All data generated here as part of dev/test should be cleaned up regularly.

    <dev|tst|lt2> env
        /mapr/atilius.sns.sky.com/tmp/btb/tmp/<daily|hourly|monthly>
        /mapr/atilius.sns.sky.com/test/maprsouth/<env>/btb/logs/
        /mapr/atilius.sns.sky.com/test/maprsouth/<env>/btb/pgdata/
        /mapr-north/data/btb/delta/

    prd env
        /mapr/flavius.sns.sky.com/tmp/btb/tmp/<daily|hourly|monthly>
        /mapr/flavius.sns.sky.com/prd/maprsouth/btb/logs/
        /mapr/flavius.sns.sky.com/prd/maprsouth/btb/pgdata/
        /mapr-north/data/btb/delta/
            
## Build
Delete Airflow docker container images using the command below.

    ./clean_docker.sh

Build Airflow and dependant packages using the command below.

    ./build_airflow.sh
    
## Deploy

Deploy Airflow container using the command below. This also setups Airflow variables, connection and authentication.

    ./deploy.sh up
    
NB : This uses environment variable "ENV" which is "dev|tst|lt2|prd".

## Teardown

Teardown Airflow container using the command below.

    ./deploy.sh down

NB: WARNING! This will wipeout everything.

## Update Airflow Variables

Update Airflow Variables (only) using the command below.

    ./deploy.sh var

NB: This updates variables from src/airflow_dags/variables/variables.json.

## Airlfow UI Links

    http://<host>:11622/admin
