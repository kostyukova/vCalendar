import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util
import swagger_server.controllers.user_controller_impl


def authenticate_user(username, password):  # noqa: E501
    """Generates token for user

     # noqa: E501

    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: str
    """
    return swagger_server.controllers.user_controller_impl.authenticate_user(username, password)


def create_user(body):  # noqa: E501
    """Create user

    Role write:users role must be granted # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: User
    """
    return swagger_server.controllers.user_controller_impl.create_user(body)


def delete_user(username):  # noqa: E501
    """Delete user

    This can only be done with write:users role. # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: ApiResponse
    """
    return swagger_server.controllers.user_controller_impl.delete_user(username)


def get_user_by_name(username):  # noqa: E501
    """Get user by user name. Role read:users role must be granted

     # noqa: E501

    :param username: The name that needs to be fetched. 
    :type username: str

    :rtype: User
    """
    return swagger_server.controllers.user_controller_impl.get_user_by_name(username)


def update_user(username, body):  # noqa: E501
    """Updated user

    This can only be done by with write:users role. # noqa: E501

    :param username: name that need to be updated
    :type username: str
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: User
    """
    return swagger_server.controllers.user_controller_impl.update_user(username, body)
