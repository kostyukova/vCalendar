import connexion
import six

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.api_response_conflict import ApiResponseConflict  # noqa: E501
from swagger_server.models.leave_days import LeaveDays  # noqa: E501
from swagger_server import util


def add_leave_days(body):  # noqa: E501
    """Add a employee LeaveDays to the system. Role write:leave_days must be granted

     # noqa: E501

    :param body: LeaveDays object that needs to be added to the system
    :type body: dict | bytes

    :rtype: LeaveDays
    """
    if connexion.request.is_json:
        body = LeaveDays.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


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
    start_date = util.deserialize_date(start_date)
    end_date = util.deserialize_date(end_date)
    return 'do some magic!'


def find_leave_days_by_date(employeeId, leave_date):  # noqa: E501
    """Finds unique LeaveDays by employee and leave date

     # noqa: E501

    :param employeeId: Employee id to filter by
    :type employeeId: int
    :param leave_date: Leave date to filter by
    :type leave_date: str

    :rtype: LeaveDays
    """
    leave_date = util.deserialize_date(leave_date)
    return 'do some magic!'


def get_leave_days_by_id(id):  # noqa: E501
    """Find LeaveDays by ID

    Returns a single LeaveDays. # noqa: E501

    :param id: ID of LeaveDays to return
    :type id: int

    :rtype: LeaveDays
    """
    return 'do some magic!'


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
