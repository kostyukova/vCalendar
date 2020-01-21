import six

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
import swagger_server.dao.leave_days_dao as dao
from sqlalchemy import text
from swagger_server import util
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.api_response_conflict import \
    ApiResponseConflict  # noqa: E501
from swagger_server.models.leave_days import LeaveDays  # noqa: E501
from swagger_server.orm import Employee as Employee_orm
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

    # check already exists
    found = dao.find_by(body.employee_id, body.start_date, body.end_date, None)
    if len(found) > 0:
        return ErrorApiResponse.LeaveDaysExistError(body.employee_id, body.start_date, body.end_date), 409
    # check employee exist
    found = Employee_orm.query.get(body.employee_id)
    if found is None:
        return ErrorApiResponse.EmployeeNotFoundError(body.employee_id), 404
    # check rules FIXME
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
    return 'do some magic!'


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
    if start_date:
        start_date = util.deserialize_date(start_date)
    if end_date:
        end_date = util.deserialize_date(end_date)
    try:
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
    if leave_date and isinstance(leave_date, str):
        leave_date = util.deserialize_date(leave_date)
    found = dao.find_by_date(employeeId, leave_date)
    if found is None:
        return ErrorApiResponse.LeaveDaysNotFoundError(employee_id=employeeId, leave_date=leave_date), 404
    return to_dto(found)


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
    if connexion.request.is_json:
        body = LeaveDays.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def to_dto(found: LeaveDays_orm):
    return LeaveDays(employee_id=found.employee_id, leave_days=found.leave_days, start_date=found.start_date, end_date=found.end_date)
