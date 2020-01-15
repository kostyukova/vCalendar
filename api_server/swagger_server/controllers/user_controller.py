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
    return AUTH_ERRORS[hasRole](role)


def delete_user(username):  # noqa: E501
    """Delete user

    This can only be done with write:users role. # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: ApiResponse
    """
    role = auth.WRITE_USERS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.delete_user(username)
    return AUTH_ERRORS[hasRole](role)


def find_all_user():  # noqa: E501
    """Finds all users. Role read:users role must be granted

     # noqa: E501


    :rtype: List[User]
    """
    role = auth.READ_USERS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.find_all_user()
    return AUTH_ERRORS[hasRole](role)


def get_user_by_name(username):  # noqa: E501
    """Get user by user name. Role read:users role must be granted

     # noqa: E501

    :param username: The name that needs to be fetched. 
    :type username: str

    :rtype: User
    """
    role = auth.READ_USERS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.get_user_by_name(username)
    return AUTH_ERRORS[hasRole](role)


def update_user(username, body):  # noqa: E501
    """Updated user

    This can only be done by with write:users role. # noqa: E501

    :param username: name that need to be updated
    :type username: str
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: User
    """
    role = auth.WRITE_USERS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.update_user(username, body)
    return AUTH_ERRORS[hasRole](role)
