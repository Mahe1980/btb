from airflow.www_rbac.security import AirflowSecurityManager
from flask_appbuilder import AppBuilder, SQLA
from flask import Flask
import os
import json

CURRENT_DIR = os.path.dirname(__file__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, security_manager_class=AirflowSecurityManager)
security_manager = appbuilder.sm

# Create roles and users from auth.json file
with open('{}/auth.json'.format(CURRENT_DIR)) as f:
    d = json.load(f)
    for username, details in d.items():
        role_name = details["role_name"]
        role_perms = details["role_perms"]
        role_vms = details["role_vms"]
        password = details["password"]
        email = details["email"]

        security_manager.init_role(role_name, role_vms, role_perms)
        role = security_manager.find_role(role_name)
        user = security_manager.find_user(username)
        if role_name != 'Admin':
            pv = security_manager.find_permission_view_menu("can_delete", "Airflow")
            security_manager.del_permission_role(role, "can delete on Airflow")
        if not user:
            security_manager.add_user(username, username, username, email, role, password)
