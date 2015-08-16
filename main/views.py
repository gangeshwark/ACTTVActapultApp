from django.core.signals import request_started
from flask import request
import flask
from flask.ext.restless import APIManager
from main import application, db
from main.models import UsersLogin, BatteryAuditTable, CableTable, CustomerDetails, NewBatteryTable, OtherDetails, \
    PendingDetails, SwitchPhysicalCheckTable, TaskTable

__author__ = 'Gangeshwar'


@application.route('/')
def hello_world():
    return 'Hello World!'


@application.route('/apiv1/v1/login_engineer')
def index():
    username = request.args.get('username')
    password = request.args.get('password')
    user = UsersLogin.query.filter_by(username=username).first()
    return user.emp_id


# Create the Flask-Restless API manager.
manager = APIManager(application, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(UsersLogin, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(BatteryAuditTable, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(CableTable, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(CustomerDetails, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(NewBatteryTable, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(PendingDetails, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(SwitchPhysicalCheckTable, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(TaskTable, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(OtherDetails, methods=['GET', 'POST', 'PUT', 'DELETE'])


#############################################################################
@application.route('/createdb')
def create_db():
    db.create_all()

    return 'Success!'


@application.route('/deletedb')
def delete_db():
    db.drop_all()
