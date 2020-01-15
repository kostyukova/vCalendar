import os

class Config(object):
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://vcalendar_user:IjkorobFic@127.0.0.1/vcalendar'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_SECRET = os.environ.get('JWT_SECRET') or 'jwt_secret_Atduassyo'
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM') or 'HS256'
    # by default token expires in 30 min
    env = os.environ.get('JWT_EXP_DELTA_SECONDS') or '1800'
    JWT_EXP_DELTA_SECONDS = int(env)
