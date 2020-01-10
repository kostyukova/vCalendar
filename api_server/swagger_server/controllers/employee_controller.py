import connexion
import six

from swagger_server.models.employee import Employee  # noqa: E501
from swagger_server import util


def add_employee(body):  # noqa: E501
    """Add a new employee to the system. Role write:employees must be granted

     # noqa: E501

    :param body: Employee object that needs to be added to the system
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Employee.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_employee(employeeId):  # noqa: E501
    """Deletes an employee

     # noqa: E501

    :param employeeId: Employee id to delete. Role write:employees must be granted
    :type employeeId: int

    :rtype: None
    """
    return 'do some magic!'


def find_all():  # noqa: E501
    """Returns all Employees registered in the system.

     # noqa: E501


    :rtype: List[Employee]
    """
    return 'do some magic!'


def find_employees_by_team_number(teamNumber):  # noqa: E501
    """Finds Employees by given team number. Role read:employees must be granted

     # noqa: E501

    :param teamNumber: Team number to filter by
    :type teamNumber: int

    :rtype: List[Employee]
    """
    return 'do some magic!'


def get_employee_by_id(employeeId):  # noqa: E501
    """Find employee by ID

    Returns a single employee. # noqa: E501

    :param employeeId: ID of empoyee to return
    :type employeeId: int

    :rtype: Employee
    """
    return 'do some magic!'


def update_employee(body):  # noqa: E501
    """Update an existing employee. Role write:employees must be granted

     # noqa: E501

    :param body: Employee object that needs to be added to the system
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Employee.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_employee_by_id(employeeId, full_name=None, position=None):  # noqa: E501
    """Updates an employee in the system with form data. Role write:employees must be granted

     # noqa: E501

    :param employeeId: ID of employee that needs to be updated
    :type employeeId: int
    :param full_name: Updated full name of the employee
    :type full_name: str
    :param position: Updated position of the employee
    :type position: str

    :rtype: None
    """
    return 'do some magic!'
