import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.api_response import ApiResponse
from swagger_server import util, db
from swagger_server.orm import User as User_orm
from flask import jsonify


def authenticate_user(username, password):  # noqa: E501
    """Generates token for user

     # noqa: E501

    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: str
    """
    return 'do some magic!'


def create_user(body):  # noqa: E501
    """Create user

    Role write:users role must be granted # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    orm = User_orm(username=body.username,
                   password=body.password, email=body.email, roles = body.roles)
    # check username already exists
    found = User_orm.query.filter_by(username=body.username).one_or_none()
    if found != None:
        return jsonify(ApiResponse(code=1001, type='user',
                                   message='User with username \'{}\' already exists'.format(body.username))), 409
    # check email already exists
    found = User_orm.query.filter_by(email=body.email).one_or_none()
    if found != None:
        return jsonify(ApiResponse(code=1002, type='user',
                                   message='User with email \'{}\' already exists'.format(body.email))), 409
    try:
        db.session.add(orm)
        db.session.commit()
        return get_user_by_name(body.username)
    except Exception as ex:
        return jsonify(ApiResponse(code=1003, type='user',
                                   message='Internal server error: {}'.format(ex))), 500

def delete_user(username):  # noqa: E501
    """Delete user

    This can only be done with write:users role. # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: None
    """
    if not username:
        return 'No username supplied', 400
    found = User_orm.query.filter_by(username=username).one_or_none()
    if found == None:
        return 'User not found', 404
    try:
        db.session.delete(found)
        db.session.commit()
        return 'Successful operation', 204
    except Exception as ex:
        return jsonify(ApiResponse(code=5002, type='user',
                                   message='Internal server error: {}'.format(ex))), 500


def get_user_by_name(username):  # noqa: E501
    """Get user by user name. Role read:users role must be granted

     # noqa: E501

    :param username: The name that needs to be fetched. 
    :type username: str

    :rtype: User
    """
    if not username:
        return 'No username supplied', 400
    found = User_orm.query.filter_by(username=username).one_or_none()
    if found == None:
        return 'User not found', 404
    result = User(
        id=found.id, username=found.username,
        password=found.password, email=found.email, roles = found.roles)
    return jsonify(result.to_dict())


def update_user(username, body):  # noqa: E501
    """Updated user

    This can only be done by with write:users role. # noqa: E501

    :param username: name that need to be updated
    :type username: str
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    if not username:
        return 'No username supplied', 400
    found = User_orm.query.filter_by(username=username).one_or_none()
    if found == None:
        return 'User not found', 404
    found.username = body.username
    found.password = body.password
    found.email = body.email
    found.roles = body.roles
    # fixme roles
    try:
        db.session.add(found)
        db.session.commit()
        return get_user_by_name(body.username)
    except Exception as ex:
        return jsonify(ApiResponse(code=5001, type='user',
                                   message='Internal server error: {}'.format(ex))), 500