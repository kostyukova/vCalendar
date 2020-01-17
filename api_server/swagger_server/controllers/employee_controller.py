import six

import connexion
import swagger_server.controllers.employee_controller_impl as impl
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
from swagger_server import auth, util
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.employee import Employee  # noqa: E501

AUTH_ERRORS = {
    auth.TokenStatus.EXPIRED: lambda role: ErrorApiResponse.TokenExpiredError(type='Employee'),
    auth.TokenStatus.INVALID: lambda role: ErrorApiResponse.TokenInvalidError(type='Employee'),
    auth.TokenStatus.NO_ROLE_GRANTED: lambda role: ErrorApiResponse.NoRoleGrantedError(role=role, type='Employee'),
    auth.TokenStatus.ROLE_GRANTED: None
}


def add_employee(body):  # noqa: E501
    """Add a new employee to the system. Role write:employees must be granted

     # noqa: E501

    :param body: Employee object that needs to be added to the system
    :type body: dict | bytes

    :rtype: Employee
    """
    role = auth.WRITE_EMPLOYEES
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.add_employee(body)
    return AUTH_ERRORS[hasRole](role)


def delete_employee(employeeId):  # noqa: E501
    """Deletes an employee. Role write:employees must be granteds

     # noqa: E501

    :param employeeId: Employee id to delete
    :type employeeId: int

    :rtype: ApiResponse
    """
    role = auth.WRITE_EMPLOYEES
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.delete_employee(employeeId)
    return AUTH_ERRORS[hasRole](role)


def find_all_employee():  # noqa: E501
    """Returns all Employees registered in the system.

     # noqa: E501


    :rtype: List[Employee]
    """
    return impl.find_all_employee()

def find_employee_by_email(email):  # noqa: E501
    """Finds Employee by given email

     # noqa: E501

    :param email: Unique employee email
    :type email: str

    :rtype: Employee
    """
    return impl.find_employee_by_email(email)


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
    :param team_id: Team id to filter by
    :type team_id: int
    :param email: Email template to filter by
    :type email: str

    :rtype: List[Employee]
    """
    return impl.find_employees_by(full_name, position, specialization, expert, team_id, email)


def get_employee_by_id(employeeId):  # noqa: E501
    """Find employee by ID

    Returns a single employee. # noqa: E501

    :param employeeId: ID of empoyee to return
    :type employeeId: int

    :rtype: Employee
    """
    return impl.get_employee_by_id(employeeId)


def update_employee_by_id(employeeId, body):  # noqa: E501
    """Updates an employee in the system with form data. Role write:employees must be granted

     # noqa: E501

    :param employeeId: ID of empoyee to return
    :type employeeId: int
    :param body: Employee object that needs to be updated in the system

    :type body: dict | bytes

    :rtype: Employee
    """
    role = auth.WRITE_EMPLOYEES
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.update_employee_by_id(employeeId, body)
    return AUTH_ERRORS[hasRole](role)
