import logging
from datetime import datetime, timedelta
from enum import Enum, auto, unique

import bcrypt
import jwt
from swagger_server import db
from swagger_server.config import Config
import swagger_server.dao.user_dao as dao

(AUTH_HEADER, PAYLOAD_USER_ID, PAYLOAD_EXP) = (
    'Authorization', 'user_id', 'exp')

(READ_USERS, WRITE_USERS, WRITE_TEAMS, WRITE_EMPLOYEES, WRITE_TOTAL_DAYS, WRITE_LEAVE_DAYS) = (
    'read:users', 'write:users', 'write:teams', 'write:employees', 'write:total_days', 'write:leave_days')

@unique
class TokenStatus(Enum):
    INVALID = ('INVALID', 401)
    EXPIRED = ('EXPIRED', 401)
    ROLE_GRANTED = ('ROLE_GRANTED', 200)
    NO_ROLE_GRANTED = ('NO_ROLE_GRANTED', 403)

    def __init__(self, title, http_status):
        self.title = title
        self.http_status = http_status

logging.basicConfig(level=logging.INFO)


def generate_token(username, password):
    found = dao.get_by_name(username)
    if found == None:
        return None
    if not check_password_hash(password, found.password):
        return None
    payload = {
        PAYLOAD_USER_ID: found.id,
        PAYLOAD_EXP: datetime.utcnow() + timedelta(seconds=Config.JWT_EXP_DELTA_SECONDS)
    }
    return jwt.encode(payload, Config.JWT_SECRET, Config.JWT_ALGORITHM).decode('utf-8')


def validate_token(token: str):
    if token:
        partns = token.split(' ')
        if len(partns) > 1:
            jwt_token = partns[1]
            logging.info('JWT token from header: %s', jwt_token)
            try:
                payload = jwt.decode(
                    jwt_token, Config.JWT_SECRET,  algorithms=[Config.JWT_ALGORITHM])
                user = dao.get(payload[PAYLOAD_USER_ID])
                return user if user else TokenStatus.INVALID
            except jwt.DecodeError:
                return TokenStatus.INVALID
            except jwt.ExpiredSignatureError:
                return TokenStatus.EXPIRED
    return TokenStatus.INVALID


def has_role(headers, role: str):
    '''
    returns 
        TokenStatus.ROLE_GRANTED if token is valid and user has specified role granted
        TokenStatus.NO_ROLE_GRANTED if token is valid but user does not have specified role granted
        TokenStatus.INVALID if given token is invalid
        TokenStatus.EXPIRED if given token has been expired
    '''
    if AUTH_HEADER not in headers:
        return TokenStatus.INVALID
    result = validate_token(headers[AUTH_HEADER])
    if not isinstance(result, TokenStatus):
        roles = result.roles.split(',')
        return TokenStatus.ROLE_GRANTED if role in roles else TokenStatus.NO_ROLE_GRANTED
    return result


def generate_password_hash(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password_hash(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode(), password_hash.encode())
