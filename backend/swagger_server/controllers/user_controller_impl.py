import six

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
import swagger_server.dao.user_dao as dao
from swagger_server import auth, db, util
from swagger_server.models.api_response import ApiResponse
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_safe import UserSafe  # noqa: E501
from swagger_server.orm import User as User_orm


def authenticate_user(username, password):  # noqa: E501
    """Generates token for user

     # noqa: E501

    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: str
    """
    token = auth.generate_token(username, password)
    if token is not None:
        return token
    else:
        return ErrorApiResponse.AuthError(), 400


def create_user(body):  # noqa: E501
    """Create user

    Role write:users role must be granted # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: UserSafe
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    orm = User_orm(username=body.username, password=auth.generate_password_hash(body.password),
                   email=body.email, roles=body.roles if body.roles else '')
    # check username already exists
    found = dao.get_by_name(body.username)
    if found is not None:
        return ErrorApiResponse.UsernameExistError(body.username), 409
    # check email already exists
    found = dao.get_by_email(body.email)
    if found is not None:
        return ErrorApiResponse.UseremailExistError(body.email), 409
    try:
        dao.persist(orm)
        return get_user_by_name(body.username)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex), 500


def delete_user(id):  # noqa: E501
    """Delete user

    This can only be done with write:users role. # noqa: E501

    :param id: The id of user that needs to be deleted
    :type id: int

    :rtype: ApiResponse
    """
    found = dao.get(id)
    if found is None:
        return ErrorApiResponse.UserNotFoundError(id=id), 404
    try:
        dao.delete(found)
        return 'Successful operation', 204
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex), 500


def find_by(username=None, email=None, roles=None):  # noqa: E501
    """Finds users by given parameters. Role read:users role must be granted

     # noqa: E501

    :param username: The username to filter by. 
    :type username: str
    :param email: The email to filter by. 
    :type email: str
    :param roles: Roles to filter by. 
    :type roles: str

    :rtype: List[UserSafe]
    """
    found = dao.find_by(username=username, email=email, roles=roles)
    return [to_user_dto(elem) for elem in found]


def get_user_by_id(id):  # noqa: E501
    """Gets user by id. Role read:users role must be granted

     # noqa: E501

    :param id: The id of user that needs to be fetched
    :type id: int

    :rtype: UserSafe
    """
    found = dao.get(id)
    if found is None:
        return ErrorApiResponse.UserNotFoundError(id=id), 404
    return to_user_dto(found)


def get_user_by_name(username):  # noqa: E501
    """Get user by user name. Role read:users role must be granted

     # noqa: E501

    :param username: The name of user that needs to be fetched. 
    :type username: str

    :type username: str

    :rtype: UserSafe
    """
    if not username:
        return ErrorApiResponse.NoUsernameError(), 400
    found = dao.get_by_name(username)
    if found is None:
        return ErrorApiResponse.UserNotFoundError(username=username), 404
    return to_user_dto(found)


def patch_user(id, body):  # noqa: E501
    """Updated user password

    This can only be done by with write:users role. # noqa: E501

    :param id: The id of user that needs to be updated
    :type id: int
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: UserSafe
    """
    found = dao.get(id)
    if found is None:
        return ErrorApiResponse.UserNotFoundError(id=id), 404
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501

    # update only password
    found.password = auth.generate_password_hash(body.password)
    try:
        dao.persist(found)
        return get_user_by_id(id)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex), 500


def update_user(id, body):  # noqa: E501
    """Updated user

    This can only be done by with write:users role. # noqa: E501

    :param id: The id of user that needs to be updated
    :type id: int
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: UserSafe
    """
    found = dao.get(id)
    if found is None:
        return ErrorApiResponse.UserNotFoundError(id=id), 404
    if connexion.request.is_json:
        body = UserSafe.from_dict(connexion.request.get_json())  # noqa: E501
    # check username already exists
    duplicate = dao.get_by_name(body.username)
    if duplicate is not None and duplicate.id != found.id:
        return ErrorApiResponse.UsernameExistError(body.username), 409
    # check email already exists
    duplicate = dao.get_by_email(body.email)
    if duplicate is not None and duplicate.id != found.id:
        return ErrorApiResponse.UseremailExistError(body.email), 409

    found.username = body.username
    found.email = body.email
    found.roles = body.roles if body.roles else ''
    try:
        dao.persist(found)
        return get_user_by_id(id)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex), 500


def to_user_dto(found):
    return UserSafe(id=found.id, username=found.username, email=found.email, roles=found.roles)
