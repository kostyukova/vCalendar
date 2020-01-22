import six

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
import swagger_server.dao.employee_dao as employee_dao
import swagger_server.dao.total_days_dao as dao
from swagger_server import auth, db, util
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.total_days import TotalDays  # noqa: E501
from swagger_server.orm import Employee_total_days as TotalDays_orm


def add_total_days(body):  # noqa: E501
    """Add a employee total days to the system. Role write:total_days must be granted

     # noqa: E501

    :param body: TotalDays object that needs to be added to the system
    :type body: dict | bytes

    :rtype: TotalDays
    """
    if connexion.request.is_json:
        body = TotalDays.from_dict(connexion.request.get_json())  # noqa: E501
    # check already exists
    found = dao.find_by_year(body.employee_id, body.year)
    if found is not None:
        return ErrorApiResponse.TotalDaysExistError(body.employee_id, body.year), 409
    employee = employee_dao.get(body.employee_id)
    if employee is None:
        return ErrorApiResponse.EmployeeNotFoundError(body.employee_id), 404
    orm = TotalDays_orm(employee_id=body.employee_id,
                        total_days=body.total_days, year=body.year)
    try:
        dao.persist(orm)
        return find_total_days_by_year(body.employee_id, body.year)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='total days'), 500


def delete_total_days(id):  # noqa: E501
    """Deletes a TotalDays. Role write:total_days must be granteds

     # noqa: E501

    :param id: TotalDays id to delete
    :type id: int

    :rtype: ApiResponse
    """
    found = dao.get(id)
    if found is None:
        return ErrorApiResponse.TotalDaysNotFoundError(id=id), 404
    try:
        dao.delete(found)
        return 'Successful operation', 204
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='total days'), 500


def find_employee_total_days(employeeId):  # noqa: E501
    """Finds TotalDays by employee

     # noqa: E501

    :param employeeId: Employee id to filter by
    :type employeeId: int

    :rtype: List[TotalDays]
    """
    employee = employee_dao.get(employeeId)
    if employee is None:
        return ErrorApiResponse.EmployeeNotFoundError(employeeId), 404
    try:
        return [to_dto(elem) for elem in dao.find_by(employeeId)]
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='total days'), 500


def find_total_days_by(employee_id=None, year=None):  # noqa: E501
    """Finds TotalDays by given parameters

     # noqa: E501

    :param employee_id: Employee id to filter by
    :type employee_id: int
    :param year: Year to filter by
    :type year: int

    :rtype: List[TotalDays]
    """
    try:
        return [to_dto(elem) for elem in dao.find_by(employee_id, year)]
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='total days'), 500


def find_total_days_by_year(employeeId, year):  # noqa: E501
    """Finds unique TotalDay by employee and year

     # noqa: E501

    :param employeeId: Employee id to filter by
    :type employeeId: int
    :param year: Year to filter by
    :type year: int

    :rtype: TotalDays
    """
    found = dao.find_by_year(employeeId, year)
    if found is None:
        return ErrorApiResponse.TotalDaysNotFoundError(employee_id=employeeId, year=year), 404
    return to_dto(found)


def get_total_days_by_id(id):  # noqa: E501
    """Find total days by ID

    Returns a single TotalDays. # noqa: E501

    :param id: ID of TotalDays to return
    :type id: int

    :rtype: TotalDays
    """
    found = dao.get(id)
    if found is None:
        return ErrorApiResponse.TotalDaysNotFoundError(id=id), 404
    return to_dto(found)


def update_total_days_by_id(id, body):  # noqa: E501
    """Updates a TotalDays in the system with form data. Role write:total_days must be granted

     # noqa: E501

    :param id: ID of TotalDays to return
    :type id: int
    :param body: TotalDays object that needs to be updated in the system
    :type body: dict | bytes

    :rtype: TotalDays
    """
    found = dao.get(id)
    if found is None:
        return ErrorApiResponse.TotalDaysNotFoundError(id=id), 404
    if connexion.request.is_json:
        body = TotalDays.from_dict(connexion.request.get_json())  # noqa: E501
    employee = employee_dao.get(body.employee_id)
    if employee is None:
        return ErrorApiResponse.EmployeeNotFoundError(body.employee_id), 404
    # check already exists
    duplicate = dao.find_by_year(body.employee_id, body.year)
    if duplicate is not None and duplicate.id != id:
        return ErrorApiResponse.TotalDaysExistError(body.employee_id, body.year), 409
    found.employee_id = body.employee_id
    found.year = body.year
    found.total_days = body.total_days
    try:
        dao.persist(found)
        return get_total_days_by_id(id)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='total days'), 500


def to_dto(found: TotalDays_orm):
    return TotalDays(id=found.id, employee_id=found.employee_id, total_days=found.total_days, year=found.year)
