from main import application, db

__author__ = 'Gangeshwar'


@application.route('/')
def hello_world():
    return 'Hello World!'


@application.route('/api/v1')
def index():
    return 'api'


#############################################################################
@application.route('/createdb')
def create_db():
    db.create_all()

    return 'Success!'


@application.route('/deletedb')
def delete_db():
    db.drop_all()
