from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from main import db
from passlib.apps import custom_app_context as pwd_context

__author__ = 'Gangeshwar'


class UsersLogin(db.Model):
    __tablename__ = 'users_login'

    # _id = db.Column(db.Integer, primary_key=True, unique=True)
    emp_id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def serialize(self):
        return {
            'emp_id': self.emp_id,
            'username': self.username,
        }

    @property
    def serialize_many2many(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        return [item.serialize for item in self.many2many]

    def __init__(self, username, password, emp_id=None):
        if emp_id is not None:
            self.emp_id = emp_id
        self.hash_password(password)  # hashing the password
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.emp_id

    def get_id(self):
        try:
            return unicode(self._id)  # python 2
        except NameError:
            return str(self._id)  # python 3


class TaskTable(db.Model):
    __tablename__ = 'task_table'
    emp_id = db.Column(db.Integer, db.ForeignKey('users_login.emp_id'), nullable=False)
    audit_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    task_assigned_date = db.Column(db.String(25))
    branch = db.Column(db.String(10))
    engineer_name = db.Column(db.String(30))
    task_location = db.Column(db.String(100))

    def __init__(self, emp_id, audit_id=None, task_assigned_date=None, branch=None, engineer_name=None,
                 task_location=None):
        self.emp_id = emp_id
        self.audit_id = audit_id
        self.task_assigned_date = task_assigned_date
        self.branch = branch
        self.engineer_name = engineer_name
        self.task_location = task_location

    @property
    def serialize(self):
        return {
            'emp_id': self.emp_id,
            'audit_id': self.audit_id,
            'task_assigned_date': self.task_assigned_date,
            'branch': self.branch,
            'engineer_name': self.engineer_name,
            'customer_name': self.customer_name,
            'customer_address': self.customer_address,
        }


class SwitchPhysicalCheckTable(db.Model):
    __tablename__ = 'switch_physical_check_table'
    _id = db.Column(db.Integer, primary_key=True, unique=True)
    audit_id = db.Column(db.Integer, db.ForeignKey('task_table.audit_id'), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('users_login.emp_id'), nullable=False)
    pre_audit_image = db.Column(db.String(100))
    cx_ip = db.Column(db.String(15))
    date = db.Column(db.String(25))
    cx_name = db.Column(db.String(30))
    cx_location = db.Column(db.String(100))
    cx_placement = db.Column(db.String(30))
    account_number = db.Column(db.Integer)
    mobile_number = db.Column(db.Integer)
    cx_cascade = db.Column(db.String(5))
    cx_rack_status = db.Column(db.String(20))
    location_premise_type = db.Column(db.String(25))
    cx_manufacturer = db.Column(db.String(15))
    cx_model = db.Column(db.String(10))
    cx_rack_condition = db.Column(db.String(25))
    rack_replaced = db.Column(db.String(5))
    lock_available = db.Column(db.String(5))
    lock_key_no = db.Column(db.String(10))
    new_lock_key_no = db.Column(db.String(10))
    ports_avail_cx = db.Column(db.Integer)
    cables_connected_cx = db.Column(db.Integer)
    extra_cables = db.Column(db.Integer)


class BatteryAuditTable(db.Model):
    __tablename__ = 'battery_audit_table'
    _id = db.Column(db.Integer, primary_key=True, unique=True)
    audit_id = db.Column(db.Integer, db.ForeignKey('task_table.audit_id'), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('users_login.emp_id'), nullable=False)
    power_sup_loc = db.Column(db.String(20))
    power_sup_sock = db.Column(db.String(20))
    battery_avail = db.Column(db.String(5))
    battery_conn_cx = db.Column(db.String(5))
    voltage = db.Column(db.String(5))
    battery_type = db.Column(db.String(5))
    capacity = db.Column(db.String(5))
    install_date = db.Column(db.String(25))
    serial = db.Column(db.Integer)
    check_point_t1 = db.Column(db.Float)  # First 15 Min Discharging Test
    check_point_t2 = db.Column(db.Float)  # Second 15 Min Discharging Test
    check_point_t3 = db.Column(db.String(5))  # Is Battery going down on Starting the Discharging Test
    is_battery_changed = db.Column(db.String(5))


class NewBatteryTable(db.Model):
    __tablename__ = 'new_battery_table'
    _id = db.Column(db.Integer, primary_key=True, unique=True)
    audit_id = db.Column(db.Integer, db.ForeignKey('task_table.audit_id'), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('users_login.emp_id'), nullable=False)
    new_battery_installed = db.Column(db.String(5))
    new_battery_type = db.Column(db.String(10))
    battery_install_date = db.Column(db.String(25))
    battery_capacity = db.Column(db.Float)
    baterry_serial = db.Column(db.String(10))
    earthing_status = db.Column(db.String(5))


class CableTable(db.Model):
    __tablename__ = 'cable_table'
    _id = db.Column(db.Integer, primary_key=True, unique=True)
    audit_id = db.Column(db.Integer, db.ForeignKey('task_table.audit_id'), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('users_login.emp_id'), nullable=False)
    is_sagging = db.Column(db.String(5))
    routing_status = db.Column(db.String(10))
    is_passing_electrical = db.Column(db.String(5))


class CustomerDetails(db.Model):
    __tablename__ = 'customer_details'
    _id = db.Column(db.Integer, primary_key=True, unique=True)
    audit_id = db.Column(db.Integer, db.ForeignKey('task_table.audit_id'), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('users_login.emp_id'), nullable=False)
    customer_name = db.Column(db.String(10))
    customer_port = db.Column(db.Integer)


class OtherDetails(db.Model):
    __tablename__ = 'other_details'
    _id = db.Column(db.Integer, primary_key=True, unique=True)
    audit_id = db.Column(db.Integer, db.ForeignKey('task_table.audit_id'), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('users_login.emp_id'), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    post_audit_image = db.Column(db.String(100))


class PendingDetails(db.Model):
    __tablename__ = 'pending_details'
    _id = db.Column(db.Integer, primary_key=True, unique=True)
    audit_id = db.Column(db.Integer, db.ForeignKey('task_table.audit_id'), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('users_login.emp_id'), nullable=False)
    connector = db.Column(db.String(5))
    switch = db.Column(db.String(5))
    jack = db.Column(db.String(5))
    others = db.Column(db.String(5))
