import json

from flask import request, session, make_response, jsonify

from main import application, db
from main.models import UsersLogin, TaskTable

__author__ = 'Gangeshwar'


@application.route('/')
def hello_world():
    return 'Hello World!'


##############################   USER  ###############################
@application.route('/api/v1/all_users', methods=['GET'])
def all_users():
    users = UsersLogin.query.all()
    data = []
    for user in users:
        data.append({
            'emp_id': user.emp_id,
            'username': user.username,
        })
    response = make_response(jsonify(users=data), 200)

    return response


@application.route('/api/v1/login', methods=['POST'])
def index():
    username = request.form.get('username', type=str)
    password = request.form.get('password', type=str)
    print(username + " " + password)
    user = UsersLogin.query.filter_by(username=username).first()
    print(user)
    if user is None:
        response = make_response(json.dumps('User doesn\'t exist. Sign up before you auth!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    user_id = user.emp_id
    if not user.verify_password(password=password):
        response = make_response(json.dumps('Username and Password doesn\'t match.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    session['emp_id'] = user.emp_id
    response = make_response(json.dumps('Login successful!'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@application.route('/api/v1/logout', methods=['POST'])
def logout():
    try:
        session.pop('emp_id')
    except Exception as e:
        return make_response(jsonify(fail="User logout failed", reason=e), 400)

    return make_response(jsonify(success="User logged out"), 200)


# only admins
@application.route('/api/v1/admin/add_admin')
def add_admin():
    admin = UsersLogin(emp_id='1', username='admin', password='admin')
    db.session.add(admin)
    db.session.commit()
    return 'Admin added'


@application.route('/api/v1/admin/add_users', methods=['POST'])
def add_user():
    username = request.form.get('username', type=str)
    password = request.form.get('password', type=str)
    user = UsersLogin.query.filter_by(username=username).first()
    if user is not None:
        return make_response(jsonify(fail="username exists"), 400)
    admin = UsersLogin(username=username, password=password)
    db.session.add(admin)
    db.session.commit()
    return make_response(jsonify(success="User added"), 200)


############################################################################################


############################ TaskTable #####################################################
@application.route('/api/v1/admin/add_task_table', methods=['POST'])
def add_task():
    emp_id = request.form.get('emp_id', type=str)
    audit_id = request.form.get('audit_id', type=str)
    task_assigned_date = request.form.get('task_date', type=str)
    branch = request.form.get('branch', type=str)
    engineer_name = request.form.get('engineer_name', type=str)
    task_location = request.form.get('task_location', type=str)
    if TaskTable.query.filter_by(audit_id=audit_id).first() is None:
        return make_response(jsonify(fail="Audit ID exists"), 400)
    task = TaskTable(emp_id, audit_id, task_assigned_date, branch, engineer_name, task_location)
    db.session.add(task)
    db.session.commit()
    return make_response(jsonify(fail="Audit added"), 200)


@application.route('/api/v1/show_task_table', methods=['GET'])
def show_list():
    if session['emp_id'] is None:
        response = make_response(jsonify(error_msg='Not authorized.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    tasks = TaskTable.query.filter_by(emp_id=session['emp_id']).all()
    data = []
    for task in tasks:
        data.append({
            'emp_id': task.emp_id,
            'audit_id': task.audit_id,
            'task_assigned_date': task.task_assigned_date,
            'branch': task.branch,
            'engineer_name': task.engineer_name,
            'task_location': task.task_location,
        })
    # return make_response(json.dumps(tasks, 200), 200)
    return make_response(jsonify(tasks=data))


@application.route('/api/v1/checkuser', methods=['GET'])
def check():
    return jsonify(session=session['emp_id'])


@application.route('/createdb')
def create_db():
    db.create_all()
    return 'Success!'


@application.route('/deletedb')
def delete_db():
    db.drop_all()
    return 'Success!'
