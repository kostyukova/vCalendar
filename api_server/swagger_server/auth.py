from datetime import datetime, timedelta
import jwt
from swagger_server import db
from swagger_server.config import Config
from swagger_server.orm import User as User_orm
from enum import Enum, auto, unique
import logging

(AUTH_HEADER, PAYLOAD_USER_ID, PAYLOAD_EXP) = (
    'Authorization', 'user_id', 'exp')

(READ_USERS, WRITE_USERS, READ_EMPLOYEES, WRITE_EMPLOYEES) = (
    'read:users', 'write:users', 'read:employees', 'write:employees')


@unique
class TokenStatus(Enum):
    INVALID = auto()
    EXPIRED = auto()
    ROLE_GRANTED = auto()
    NO_ROLE_GRANTED = auto()


logging.basicConfig(level=logging.INFO)


def generate_token(username, password):
    found = User_orm.query.filter_by(username=username).one_or_none()
    if found == None:
        return None
    if found.password != password:  # FIXME password hash
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
                return User_orm.query.filter_by(id=payload[PAYLOAD_USER_ID]).one_or_none()
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
