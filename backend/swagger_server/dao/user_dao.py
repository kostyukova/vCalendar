from datetime import date

from sqlalchemy import text
from swagger_server import db, util
from swagger_server.orm import User as User_orm


def find_by(username: str = None, email: str = None, roles: str = None):
    """Finds all users. Role read:users role must be granted

    :rtype: List[User_orm]
    """
    query = User_orm.query
    if username and username.strip():
        query = query.filter(User_orm.username.ilike(
            '%' + username.strip() + '%'))
    if email and email.strip():
        query = query.filter(User_orm.email.ilike(
            '%' + email.strip() + '%'))
    if roles and roles.strip():
        query = query.filter(User_orm.roles.ilike(
            '%' + roles.strip() + '%'))

    return query.all()


def get_by_name(username):
    """Get user by user name. Role read:users role must be granted

    :param username: The name to find by. 
    :type username: str

    :rtype: User_orm
    """
    return User_orm.query.filter_by(username=username).one_or_none()


def get_by_email(email):
    """Get user by email. Role read:users role must be granted

    :param email: The email to find by. 
    :type email: str

    :rtype: User_orm
    """
    return User_orm.query.filter_by(email=email).one_or_none()


def get(id):
    """Gets User by id

    :param id: User id
    :type id: int

    :rtype: User_orm
    """
    return User_orm.query.get(id)


def persist(orm: User_orm):
    """Persists given orm

    :param orm: User object to persist
    :type orm: User_orm

    """
    db.session.add(orm)
    db.session.commit()


def delete(orm: User_orm):
    """Deletes given orm

    :param orm: User object to delete
    :type orm: User_orm

    """
    db.session.delete(orm)
    db.session.commit()
