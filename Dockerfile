# VERSION 1.10.2
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow

FROM python:3.6-slim
LABEL maintainer="Puckel_"

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.10.2
ARG AIRFLOW_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ARG UID=1000
ARG GID=1001

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8
ENV AIRFLOW_GPL_UNIDECODE=yes
ENV AIRFLOW_HOME=${AIRFLOW_HOME}

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
        python3-dev \
        libxml2-dev \
        libxslt1-dev \
        libldap2-dev \
        libsasl2-dev \
        libffi-dev \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
        vim \
        tar \
        unzip \
    && apt-get update -yqq \
    && apt-get install -yqq \
         unixodbc \
         unixodbc-dev \
         libaio1 \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && usermod -u ${UID} airflow \
    && groupmod -g ${GID} airflow \
    && pip install pip setuptools wheel \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install psycopg2 \
    && pip install psycopg2-binary \
    && pip install py-postgresql \
    && pip install flask_bcrypt \
    && pip install flask-appbuilder \
    && pip install apache-airflow[crypto,postgres,hive,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
    && pip install pyodbc \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean

COPY docker/entrypoint.sh /entrypoint.sh
COPY requirements.txt /requirements.txt
COPY src/airflow_dags/config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY src/airflow_dags/config/webserver_config.py ${AIRFLOW_HOME}/webserver_config.py
COPY docker/nz.tar.gz /tmp/
COPY docker/instantclient-basic-linux.x64-18.3.0.0.0dbru.zip /tmp/
COPY docker/odbcinst.ini /etc/
COPY docker/.peanuts ${AIRFLOW_HOME}/

RUN chmod 666 /etc/odbcinst.ini
RUN $(which pip) install -I -r /requirements.txt
RUN unzip /tmp/instantclient-basic-linux.x64-18.3.0.0.0dbru.zip -d /opt/oracle/ \
    && tar -xvf /tmp/nz.tar.gz -C /opt/ \
    && export ORACLE_BASE=/opt/oracle \
    && export ORACLE_HOME=$ORACLE_BASE/instantclient_18_3 \
    && export ODBCINI=/etc/odbc.ini \
    && export NZ_ODBC_INI_PATH=/etc \
    && export NETEZZA=/opt/nz \
    && export LD_LIBRARY_PATH=$ORACLE_HOME:$NETEZZA/lib64:/usr/lib:$LD_LIBRARY_PATH \
    && export PYTHONPATH=$AIRFLOW_HOME \
    && export PATH=$NETEZZA:$PATH \
    && sh -c "echo /opt/oracle/instantclient_18_3 > /etc/ld.so.conf.d/oracle-instantclient.conf" \
    && ldconfig \
    && rm -f /tmp/instantclient-basic-linux.x64-18.3.0.0.0dbru.zip \
    && rm -f /tmp/nz.tar.gz

RUN chown -R airflow: ${AIRFLOW_HOME}
RUN chmod 755 /entrypoint.sh
EXPOSE 11622 5555 8793

USER airflow
WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"] # set default arg for entrypoint
WORKDIR ${AIRFLOW_HOME}
