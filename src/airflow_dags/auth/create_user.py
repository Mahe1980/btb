from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
from src.settings import envs
import argparse
import logging
from src.settings import log_config

# Setting up module from __file__ as the interpreter sets __name__ as __main__ when the source file is executed as
# main program
logger = logging.getLogger(name=__file__.replace(envs.PROJECT_ROOT, '').replace('/', '.')[1:-3])


def main(username, password, email, superuser):
    try:
        user = PasswordUser(models.User())
        user.username = username
        user.email = email
        user.password = password
        user.superuser = superuser
        session = settings.Session()
        session.add(user)
        session.commit()
        session.close()
    except Exception as e:
        logger.error("Unable to create airflow user '{}'".format(username))
        logger.error(str(e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', default='admin', help='username for the authentication')
    parser.add_argument('--password', default='admin', help='password for the authentication')
    parser.add_argument('--email', default='SNSDataWarehouseRequests@sky.uk', help='email id for the user')
    parser.add_argument('--superuser', default=True, help='Is it a superuser?')

    args = parser.parse_args()
    main(**vars(args))
