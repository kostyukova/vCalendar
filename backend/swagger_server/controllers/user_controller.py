import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util, auth
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
import swagger_server.controllers.user_controller_impl as impl


AUTH_ERRORS = {
    auth.TokenStatus.EXPIRED: lambda role: ErrorApiResponse.TokenExpiredError(),
    auth.TokenStatus.INVALID: lambda role: ErrorApiResponse.TokenInvalidError(),
    auth.TokenStatus.NO_ROLE_GRANTED: lambda role: ErrorApiResponse.NoRoleGrantedError(role),
    auth.TokenStatus.ROLE_GRANTED: None
}


def authenticate_user(username, password):  # noqa: E501
    """Generates token for an user

     # noqa: E501

    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: str
    """
    return impl.authenticate_user(username, password)


def create_user(body):  # noqa: E501
    """Create user

    Role write:users role must be granted # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: User
    """
    role = auth.WRITE_USERS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.create_user(body)
    return AUTH_ERRORS[hasRole](role), 401


def delete_user(id):  # noqa: E501
    """Delete user

    This can only be done with write:users role. # noqa: E501

    :param id: The id of user that needs to be deleted
    :type id: int

    :rtype: ApiResponse
    """
    role = auth.WRITE_USERS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.delete_user(id)
    return AUTH_ERRORS[hasRole](role), 401


def find_by(username=None, email=None):  # noqa: E501
    """Finds users by given parameters. Role read:users role must be granted

     # noqa: E501

    :param username: The username to filter by. 
    :type username: str
    :param email: The email to filter by. 
    :type email: str

    :rtype: List[User]
    """
    role = auth.READ_USERS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.find_by(username, email)
    return AUTH_ERRORS[hasRole](role), 401


def get_user_by_id(id):  # noqa: E501
    """Gets user by id. Role read:users role must be granted

     # noqa: E501

    :param id: The id of user that needs to be fetched
    :type id: int

    :rtype: User
    """
    role = auth.READ_USERS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.get_user_by_id(id)
    return AUTH_ERRORS[hasRole](role), 401


def get_user_by_name(username):  # noqa: E501
    """Gets user by user name. Role read:users role must be granted

     # noqa: E501

    :param username: The name of user that needs to be fetched.
    :type username: str

    :rtype: User
    """
    role = auth.READ_USERS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.get_user_by_name(username)
    return AUTH_ERRORS[hasRole](role), 401


def update_user(id, body):  # noqa: E501
    """Updated user

    This can only be done by with write:users role. # noqa: E501

    :param id: The id of user that needs to be updated
    :type id: int
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: User
    """
    role = auth.WRITE_USERS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.update_user(id, body)
    return AUTH_ERRORS[hasRole](role), 401
