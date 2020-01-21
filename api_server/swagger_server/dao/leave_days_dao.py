
from sqlalchemy import text
from swagger_server import db, util
from swagger_server.orm import Employee as Employee_orm
from swagger_server.orm import Employee_leave_days as LeaveDays_orm


def find_by(employee_id=None, start_date=None, end_date=None, year=None):
    """Finds LeaveDays by given parameters

    :param employee_id: Employee id to filter by
    :type employee_id: int
    :param start_date: Start date to filter by
    :type start_date: str
    :param end_date: End date to filter by
    :type end_date: str
    :param year: Year to filter by
    :type year: int

    :rtype: List[LeaveDays_orm]
    """
    query = LeaveDays_orm.query
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if start_date:
        query = query.filter(text("end_date >= :start_date"))\
            .params(start_date=start_date)
    if end_date:
        query = query.filter(text("start_date <= :end_date"))\
            .params(end_date=end_date)
    if year:
        query = query.filter(text("year(start_date) = :year or year(end_date) = :year"))\
            .params(year=year)
    return query.all()


def find_by_date(employeeId, leave_date):
    """Finds unique LeaveDays by employee and leave date

    :param employeeId: Employee id to filter by
    :type employeeId: int
    :param leave_date: Leave date to filter by
    :type leave_date: str

    :rtype: LeaveDays_orm
    """
    return LeaveDays_orm.query.filter_by(employee_id=employeeId)\
        .filter(text(":param between start_date and end_date"))\
        .params(param=leave_date).one_or_none()


def get(id):
    """Gets unique LeaveDays by id

    :param id: LeaveDays id
    :type id: int

    :rtype: LeaveDays_orm
    """
    return LeaveDays_orm.query.get(id)


def persist(orm: LeaveDays_orm):
    """Persists given orm

    :param orm: LeaveDays object to persist
    :type orm: LeaveDays_orm

    """
    db.session.add(orm)
    db.session.commit()
