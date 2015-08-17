__author__ = 'GANGESHWAR'
import os

APP_DEBUG = True

CSRF_ENABLED = True
SECRET_KEY = '!@#!!!travbro_secretkeyyoucannotdecode1234!!!'

basedir = os.path.abspath(os.path.dirname(__file__))
# 'mysql://root:root@localhost:3306/actapult'
# SQLALCHEMY_DATABASE_URI = 'mysql://travbroadmin:travbro123admin@aa2w99jq31wdvg.cxchmrq28t81.us-east-1.rds.amazonaws.com/travbrodb'
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/actapult' if os.environ.get(
    'SQLALCHEMY_DATABASE_URI') is None else os.environ.get('SQLALCHEMY_DATABASE_URI')

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'main.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SERVER_NAME = 'localhost:5000' if os.environ.get('SERVER_NAME') is None else os.environ.get('SERVER_NAME')

# mysql://actapult:actapult@aa1how0gdmr52oh.c7aitaarf7z4.us-east-1.rds.amazonaws.com/actapult
