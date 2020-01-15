import six

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
from flask import jsonify
from swagger_server import auth, db, util
from swagger_server.models.api_response import ApiResponse
from swagger_server.models.user import User  # noqa: E501
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
        return jsonify(ErrorApiResponse.AuthError()), 400


def create_user(body):  # noqa: E501
    """Create user

    Role write:users role must be granted # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    orm = User_orm(username=body.username, password=auth.generate_password_hash(body.password),
                   email=body.email, roles=body.roles)
    # check username already exists
    found = User_orm.query.filter_by(username=body.username).one_or_none()
    if found is not None:
        return jsonify(ErrorApiResponse.UsernameExistError(body.username)), 409
    # check email already exists
    found = User_orm.query.filter_by(email=body.email).one_or_none()
    if found is not None:
        return jsonify(ErrorApiResponse.UseremailExistError(body.email)), 409
    try:
        db.session.add(orm)
        db.session.commit()
        return get_user_by_name(body.username)
    except Exception as ex:
        return jsonify(ErrorApiResponse.InternalServerError(ex)), 500


def delete_user(username):  # noqa: E501
    """Delete user

    This can only be done with write:users role. # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: None
    """
    if not username:
        return jsonify(ErrorApiResponse.NoUsernameError()), 400
    found = User_orm.query.filter_by(username=username).one_or_none()
    if found is None:
        return jsonify(ErrorApiResponse.UserNotFoundError()), 404
    try:
        db.session.delete(found)
        db.session.commit()
        return 'Successful operation', 204
    except Exception as ex:
        return jsonify(ErrorApiResponse.InternalServerError()), 500


def find_all_user():  # noqa: E501
    """Finds all users. Role read:users role must be granted

     # noqa: E501


    :rtype: List[User]
    """
    found = User_orm.query.all()
    return [to_user_dto(elem) for elem in found]


def get_user_by_name(username):  # noqa: E501
    """Get user by user name. Role read:users role must be granted

     # noqa: E501

    :param username: The name that needs to be fetched. 
    :type username: str

    :rtype: User
    """
    if not username:
        return jsonify(ErrorApiResponse.NoUsernameError()), 400
    found = User_orm.query.filter_by(username=username).one_or_none()
    if found is None:
        return jsonify(ErrorApiResponse.UserNotFoundError()), 404
    return jsonify(to_user_dto(found).to_dict())


def update_user(username, body):  # noqa: E501
    """Updated user

    This can only be done by with write:users role. # noqa: E501

    :param username: name that need to be updated
    :type username: str
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: None
    """
    if not username:
        return jsonify(ErrorApiResponse.NoUsernameError()), 400
    found = User_orm.query.filter_by(username=username).one_or_none()
    if found is None:
        return jsonify(ErrorApiResponse.UserNotFoundError()), 404
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501

    found.username = body.username
    found.password = auth.generate_password_hash(body.password)
    found.email = body.email
    found.roles = body.roles
    try:
        db.session.add(found)
        db.session.commit()
        return get_user_by_name(body.username)
    except Exception as ex:
        return jsonify(ErrorApiResponse.InternalServerError()), 500


def to_user_dto(found):
    return User(id=found.id, username=found.username, password='***', email=found.email, roles=found.roles)
