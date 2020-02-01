from datetime import date

from sqlalchemy import text
from swagger_server import db, util
from swagger_server.orm import Team as Team_orm


def find_by(name=None):
    """Finds Teams by given parameters

    :param name: Team name template to filter by
    :type name: str

    :rtype: List[Team_orm]
    """
    query = Team_orm.query
    if name and name.strip():
        query = query.filter(Team_orm.name.ilike(
            '%' + name.strip() + '%'))
    return query.all()


def find_by_name(name):
    """Finds Team by name

    :param name: Team name to find
    :type name: str

    :rtype: Team_orm
    """
    return Team_orm.query.filter_by(name=name).one_or_none()


def get(id):
    """Gets Team by id

    :param id: Team id
    :type id: int

    :rtype: Team_orm
    """
    return Team_orm.query.get(id)


def persist(orm: Team_orm):
    """Persists given orm

    :param orm: Team object to persist
    :type orm: Team_orm

    """
    db.session.add(orm)
    db.session.commit()


def delete(orm: Team_orm):
    """Deletes given orm

    :param orm: Team object to delete
    :type orm: Team_orm

    """
    db.session.delete(orm)
    db.session.commit()
