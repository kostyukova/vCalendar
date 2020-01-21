from datetime import date

from sqlalchemy import text
from swagger_server import db, util
from swagger_server.orm import Employee as Employee_orm


def get(id):
    """Gets Employee by id

    :param id: Employee id
    :type id: int

    :rtype: Employee_orm
    """
    return Employee_orm.query.get(id)


def persist(orm: Employee_orm):
    """Persists given orm

    :param orm: Employee object to persist
    :type orm: Employee_orm

    """
    db.session.add(orm)
    db.session.commit()


def delete(orm: Employee_orm):
    """Deletes given orm

    :param orm: Employee object to delete
    :type orm: Employee_orm

    """
    db.session.delete(orm)
    db.session.commit()
