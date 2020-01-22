import six

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
import swagger_server.dao.employee_dao as dao
import swagger_server.dao.team_dao as team_dao
from swagger_server import db, util
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.employee import Employee  # noqa: E501
from swagger_server.orm import Employee as Employee_orm


def add_employee(body):  # noqa: E501
    """Add a new employee to the system. Role write:employees must be granted

     # noqa: E501

    :param body: Employee object that needs to be added to the system
    :type body: dict | bytes

    :rtype: Employee
    """
    if connexion.request.is_json:
        body = Employee.from_dict(connexion.request.get_json())  # noqa: E501
    # check email already exists
    found = dao.find_by_email(body.email)
    if found is not None:
        return ErrorApiResponse.EmployeeEmailExistError(body.email), 409
    # check for team number
    team = team_dao.get(body.team_id)
    if team is None:
        return ErrorApiResponse.TeamNotFoundError(id=body.team_id), 404
    # persist new employee
    orm = Employee_orm(full_name=body.full_name, position=body.position,
                       specialization=body.specialization if body.specialization else '',
                       team_id=body.team_id, expert=body.expert, email=body.email)
    try:
        dao.persist(orm)
        return find_employee_by_email(body.email)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='employee'), 500


def delete_employee(employeeId):  # noqa: E501
    """Deletes an employee. Role write:employees must be granteds

     # noqa: E501

    :param employeeId: Employee id to delete
    :type employeeId: int

    :rtype: ApiResponse
    """
    found = dao.get(employeeId)
    if found is None:
        return ErrorApiResponse.EmployeeNotFoundError(id=employeeId), 404
    try:
        dao.delete(found)
        return 'Successful operation', 204
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='employee'), 500


def find_employees_by(full_name=None, position=None, specialization=None, expert=None, team_id=None, email=None):  # noqa: E501
    """Finds Employees by given parameters

     # noqa: E501

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
    try:
        return [to_employee_dto(elem) for elem in dao.find_by(full_name, position, specialization, expert, team_id, email)]
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='employee'), 500


def find_employee_by_email(email):  # noqa: E501
    """Finds Employee by given email

     # noqa: E501

    :param email: Unique employee email
    :type email: str

    :rtype: Employee
    """
    found = dao.find_by_email(email)
    if found is None:
        return ErrorApiResponse.EmployeeNotFoundError(email=email), 404
    return to_employee_dto(found)


def get_employee_by_id(employeeId):  # noqa: E501
    """Find employee by ID

    Returns a single employee. # noqa: E501

    :param employeeId: ID of empoyee to return
    :type employeeId: int

    :rtype: Employee
    """
    found = dao.get(employeeId)
    if found is None:
        return ErrorApiResponse.EmployeeNotFoundError(id=employeeId), 404
    return to_employee_dto(found)


def update_employee_by_id(employeeId, body):  # noqa: E501
    """Updates an employee in the system with form data. Role write:employees must be granted

     # noqa: E501

    :param employeeId: ID of empoyee to return
    :type employeeId: int
    :param body: Employee object that needs to be added to the system
    :type body: dict | bytes

    :rtype: Employee
    """
    found = dao.get(employeeId)
    if found is None:
        return ErrorApiResponse.EmployeeNotFoundError(id=employeeId), 404
    if connexion.request.is_json:
        body = Employee.from_dict(connexion.request.get_json())  # noqa: E501
    # check email already exists
    duplicate = dao.find_by_email(body.email)
    if duplicate is not None and duplicate.employee_id != body._employee_id:
        return ErrorApiResponse.EmployeeEmailExistError(body.email), 409
    # check for team number
    team = team_dao.get(body.team_id)
    if team is None:
        return ErrorApiResponse.TeamNotFoundError(id=body.team_id), 404
    found.full_name = body.full_name
    found.position = body.position
    found.specialization = body.specialization if body.specialization else ''
    found.team_id = body.team_id
    found.expert = body.expert
    found.email = body.email
    try:
        dao.persist(found)
        return get_employee_by_id(employeeId)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='employee'), 500


def to_employee_dto(found: Employee_orm):
    return Employee(employee_id=found.employee_id, full_name=found.full_name, position=found.position,
                    specialization=found.specialization, team_id=found.team_id,
                    expert=found.expert, email=found.email)
