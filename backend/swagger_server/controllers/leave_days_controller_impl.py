import six

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
import swagger_server.controllers.rules as rules
import swagger_server.dao.employee_dao as employee_dao
import swagger_server.dao.leave_days_dao as dao
from sqlalchemy import text
from swagger_server import util
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.api_response_conflict import \
    ApiResponseConflict  # noqa: E501
from swagger_server.models.leave_days import LeaveDays  # noqa: E501
from swagger_server.orm import Employee_leave_days as LeaveDays_orm


def add_leave_days(body):  # noqa: E501
    """Add a employee LeaveDays to the system. Role write:leave_days must be granted

     # noqa: E501

    :param body: LeaveDays object that needs to be added to the system
    :type body: dict | bytes

    :rtype: LeaveDays
    """
    if connexion.request.is_json:
        body = LeaveDays.from_dict(connexion.request.get_json())  # noqa: E501
    delta = body.end_date - body.start_date
    if delta.days < 0:
        return ErrorApiResponse.LeaveDaysPeriodError(body.start_date, body.end_date), 409
    # check already exists
    found = dao.find_by(body.employee_id, body.start_date, body.end_date, None)
    if len(found) > 0:
        return ErrorApiResponse.LeaveDaysExistError(body.employee_id, body.start_date, body.end_date), 409
    # check employee exist
    found = employee_dao.get(body.employee_id)
    if found is None:
        return ErrorApiResponse.EmployeeNotFoundError(body.employee_id), 404

    # check rules FIXME
    conflict = rules.check_rules(
        body.employee_id, body.start_date, body.end_date)
    if len(conflict) > 0:
        return ApiResponseConflict(code=5000, type='leave days', message='Restrictions are violated', details=conflict), 409
    orm = LeaveDays_orm(employee_id=body.employee_id,
                        leave_days=body.leave_days, start_date=body.start_date, end_date=body.end_date)
    try:
        dao.persist(orm)
        return find_leave_days_by_date(body.employee_id, body.start_date)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='leave days'), 500


def delete_leave_days(id):  # noqa: E501
    """Deletes a LeaveDays. Role write:leave_days must be granteds

     # noqa: E501

    :param id: LeaveDays id to delete
    :type id: int

    :rtype: ApiResponse
    """
    found = dao.get(id)
    if found is None:
        return ErrorApiResponse.LeaveDaysNotFoundError(id=id), 404
    try:
        dao.delete(found)
        return 'Successful operation', 204
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='leave days'), 500


def find_employee_leave_days(employeeId):  # noqa: E501
    """Finds LeaveDays by employee

     # noqa: E501

    :param employeeId: Employee id to filter by
    :type employeeId: int

    :rtype: List[LeaveDays]
    """
    # check employee exist
    employee = employee_dao.get(employeeId)
    if employee is None:
        return ErrorApiResponse.EmployeeNotFoundError(employeeId), 404
    try:
        return [to_dto(elem) for elem in dao.find_by(employeeId)]
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='leave days'), 500


def find_leave_days_by(employee_id=None, start_date=None, end_date=None, year=None):  # noqa: E501
    """Finds LeaveDays by given parameters

     # noqa: E501

    :param employee_id: Employee id to filter by
    :type employee_id: int
    :param start_date: Start date to filter by
    :type start_date: str
    :param end_date: End date to filter by
    :type end_date: str
    :param year: Year to filter by
    :type year: int

    :rtype: List[LeaveDays]
    """
    try:
        if start_date and isinstance(start_date, str):
            start_date = util.deserialize_date(start_date)
        if end_date and isinstance(end_date, str):
            end_date = util.deserialize_date(end_date)
        return [to_dto(elem) for elem in dao.find_by(employee_id, start_date, end_date, year)]
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='leave days'), 500


def find_leave_days_by_date(employeeId, leave_date):  # noqa: E501
    """Finds unique LeaveDays by employee and leave date

     # noqa: E501

    :param employeeId: Employee id to filter by
    :type employeeId: int
    :param leave_date: Leave date to filter by
    :type leave_date: str

    :rtype: LeaveDays
    """
    try:
        if leave_date and isinstance(leave_date, str):
            leave_date = util.deserialize_date(leave_date)
        found = dao.find_by_date(employeeId, leave_date)
        if found is None:
            return ErrorApiResponse.LeaveDaysNotFoundError(employee_id=employeeId, leave_date=leave_date), 404
        return to_dto(found)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='leave days'), 500



def get_leave_days_by_id(id):  # noqa: E501
    """Find LeaveDays by ID

    Returns a single LeaveDays. # noqa: E501

    :param id: ID of LeaveDays to return
    :type id: int

    :rtype: LeaveDays
    """
    found = dao.get(id)
    if found is None:
        return ErrorApiResponse.LeaveDaysNotFoundError(id=id), 404
    return to_dto(found)


def update_leave_days_by_id(id, body):  # noqa: E501
    """Updates a LeaveDays in the system with form data. Role write:leave_days must be granted

     # noqa: E501

    :param id: ID of LeaveDays to return
    :type id: int
    :param body: LeaveDays object that needs to be updated in the system
    :type body: dict | bytes

    :rtype: LeaveDays
    """
    found = dao.get(id)
    if found is None:
        return ErrorApiResponse.LeaveDaysNotFoundError(id=id), 404
    if connexion.request.is_json:
        body = LeaveDays.from_dict(connexion.request.get_json())  # noqa: E501
    delta = body.end_date - body.start_date
    if delta.days < 0:
        return ErrorApiResponse.LeaveDaysPeriodError(body.start_date, body.end_date), 409
    # check already exists
    duplicate = find_leave_days_by(
        body.employee_id, body.start_date, body.end_date)
    if len(duplicate) > 1 or (len(duplicate) == 1 and duplicate[0].id != id):
        return ErrorApiResponse.LeaveDaysExistError(body.employee_id, body.start_date, body.end_date), 409
    # check employee exist
    employee = employee_dao.get(body.employee_id)
    if employee is None:
        return ErrorApiResponse.EmployeeNotFoundError(body.employee_id), 404
    # check rules
    conflict = rules.check_rules(
        body.employee_id, body.start_date, body.end_date, id)
    if len(conflict) > 0:
        return ApiResponseConflict(code=5000, type='leave days', message='Restrictions are violated', details=conflict), 409
    found.employee_id = body.employee_id
    found.start_date = body.start_date
    found.end_date = body.end_date
    found.leave_date = body.leave_days
    try:
        dao.persist(found)
        return get_leave_days_by_id(id)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='leave days'), 500


def to_dto(found: LeaveDays_orm):
    return LeaveDays(id=found.id, employee_id=found.employee_id, leave_days=found.leave_days,
                     start_date=found.start_date, end_date=found.end_date)
