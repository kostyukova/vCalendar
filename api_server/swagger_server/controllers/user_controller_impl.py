import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util
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
    return 'do some magic!'


def delete_user(username):  # noqa: E501
    """Delete user

    This can only be done with write:users role. # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: None
    """
    return 'do some magic!'


def get_user_by_name(username):  # noqa: E501
    """Get user by user name. Role read:users role must be granted

     # noqa: E501

    :param username: The name that needs to be fetched. 
    :type username: str

    :rtype: User
    """
    found = User_orm.query.filter_by(username=username).first()
    result = User()
    result.id = found.id
    result.username = found.username
    result.password = found.password
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
    return 'do some magic!'
