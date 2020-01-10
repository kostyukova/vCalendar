import os

class Config(object):
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:pass@127.0.0.1/vcalendar'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
