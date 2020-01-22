from datetime import date

from sqlalchemy import text
from swagger_server import db, util
from swagger_server.orm import Employee_total_days as TotalDays_orm


def find_by(employee_id=None, year=None):
    """Finds TotalDays by given parameters

    :param employee_id: Employee id to filter by
    :type employee_id: int
    :param year: Year to filter by
    :type year: int

    :rtype: List[TotalDays_orm]
    """
    query = TotalDays_orm.query
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if year:
        query = query.filter_by(year=year)
    return query.all()


def find_by_year(employeeId, year):
    """Finds unique TotalDay by employee and year

    :param employeeId: Employee id to filter by
    :type employeeId: int
    :param year: Year to filter by
    :type year: int

    :rtype: TotalDays_orm
    """
    return TotalDays_orm.query.filter_by(
        employee_id=employeeId, year=year).one_or_none()


def get(id):
    """Gets TotalDays by id

    :param id: TotalDays id
    :type id: int

    :rtype: TotalDays_orm
    """
    return TotalDays_orm.query.get(id)


def persist(orm: TotalDays_orm):
    """Persists given orm

    :param orm: TotalDays object to persist
    :type orm: TotalDays_orm

    """
    db.session.add(orm)
    db.session.commit()


def delete(orm: TotalDays_orm):
    """Deletes given orm

    :param orm: TotalDays object to delete
    :type orm: TotalDays_orm

    """
    db.session.delete(orm)
    db.session.commit()
