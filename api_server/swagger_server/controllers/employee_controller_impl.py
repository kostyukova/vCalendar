import six

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
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
    orm = Employee_orm(full_name=body.full_name, position=body.position,
                       specialization=body.specialization if body.specialization else '',
                       team_id=body.team_id, expert=body.expert, email=body.email)
    # check email already exists
    found = Employee_orm.query.filter_by(email=body.email).one_or_none()
    if found is not None:
        return ErrorApiResponse.EmployeeEmailExistError(body.email), 409
    try:
        db.session.add(orm)
        db.session.commit()
        return find_employee_by_email(body.email)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='Employee'), 500


def delete_employee(employeeId):  # noqa: E501
    """Deletes an employee. Role write:employees must be granteds

     # noqa: E501

    :param employeeId: Employee id to delete
    :type employeeId: int

    :rtype: ApiResponse
    """
    found = Employee_orm.query.get(employeeId)
    if found is None:
        return ErrorApiResponse.EmployeeNotFoundError(id=employeeId), 404
    try:
        db.session.delete(found)
        db.session.commit()
        return 'Successful operation', 204
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='Employee'), 500


def find_all_employee():  # noqa: E501
    """Returns all Employees registered in the system.

     # noqa: E501


    :rtype: List[Employee]
    """
    found = Employee_orm.query.all()
    return [to_employee_dto(elem) for elem in found]


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
    try:
        return [to_employee_dto(elem) for elem in query.all()]
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='Employee'), 500


def find_employee_by_email(email):  # noqa: E501
    """Finds Employee by given email

     # noqa: E501

    :param email: Unique employee email
    :type email: str

    :rtype: Employee
    """
    found = Employee_orm.query.filter_by(email=email).one_or_none()
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
    found = Employee_orm.query.get(employeeId)
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
    found = Employee_orm.query.get(employeeId)
    if found is None:
        return ErrorApiResponse.EmployeeNotFoundError(id=employeeId), 404
    if connexion.request.is_json:
        body = Employee.from_dict(connexion.request.get_json())  # noqa: E501

    found.full_name = body.full_name
    found.position = body.position
    found.specialization = body.specialization if body.specialization else ''
    found.team_id = body.team_id
    found.expert = body.expert
    found.email = body.email
    try:
        db.session.add(found)
        db.session.commit()
        return get_employee_by_id(employeeId)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='Employee'), 500


def to_employee_dto(found: Employee_orm):
    return Employee(employee_id=found.employee_id, full_name=found.full_name, position=found.position,
                    specialization=found.specialization, team_id=found.team_id,
                    expert=found.expert, email=found.email)
