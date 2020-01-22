from datetime import date

from sqlalchemy import text
from swagger_server import db, util
from swagger_server.orm import Employee as Employee_orm


def find_by(full_name=None, position=None, specialization=None, expert=None, team_id=None, email=None):
    """Finds Employees by given parameters

    :param full_name: Full name template to filter by
    :type full_name: str
    :param position: Position template to filter by
    :type position: str
    :param specialization: Specialization template to filter by
    :type specialization: str
    :param expert: Expert mark to filter by
    :type expert: bool
    :param team_id: Team number to filter by
    :type team_id: int
    :param email: Email template to filter by
    :type email: str

    :rtype: List[Employee]
    """
    query = Employee_orm.query
    if full_name and full_name.strip():
        query = query.filter(Employee_orm.full_name.ilike(
            '%' + full_name.strip() + '%'))
    if position and position.strip():
        query = query.filter(Employee_orm.position.ilike(
            '%' + position.strip() + '%'))
    if specialization and specialization.strip():
        query = query.filter(Employee_orm.specialization.ilike(
            '%' + specialization.strip() + '%'))
    if expert is not None:
        query = query.filter_by(expert=expert)
    if team_id:
        query = query.filter_by(team_id=team_id)
    if email and email.strip():
        query = query.filter(Employee_orm.email.ilike(
            '%' + email.strip() + '%'))
    return query.all()


def find_by_email(email):
    """Finds Employee by given email

    :param email: Unique employee email
    :type email: str

    :rtype: Employee
    """
    return Employee_orm.query.filter_by(email=email).one_or_none()


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
