import six

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
import swagger_server.controllers.leave_days_controller_impl as impl
from swagger_server import auth, util
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.api_response_conflict import ApiResponseConflict  # noqa: E501
from swagger_server.models.leave_days import LeaveDays  # noqa: E501

AUTH_ERRORS = {
    auth.TokenStatus.EXPIRED: lambda role: ErrorApiResponse.TokenExpiredError(type='leave days'),
    auth.TokenStatus.INVALID: lambda role: ErrorApiResponse.TokenInvalidError(type='leave days'),
    auth.TokenStatus.NO_ROLE_GRANTED: lambda role: ErrorApiResponse.NoRoleGrantedError(role=role, type='leave days'),
    auth.TokenStatus.ROLE_GRANTED: None
}

def add_leave_days(body):  # noqa: E501
    """Add a employee LeaveDays to the system. Role write:leave_days must be granted

     # noqa: E501

    :param body: LeaveDays object that needs to be added to the system
    :type body: dict | bytes

    :rtype: LeaveDays
    """
    role = auth.WRITE_LEAVE_DAYS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.add_leave_days(body)
    return AUTH_ERRORS[hasRole](role)


def delete_leave_days(id):  # noqa: E501
    """Deletes a LeaveDays. Role write:leave_days must be granteds

     # noqa: E501

    :param id: LeaveDays id to delete
    :type id: int

    :rtype: ApiResponse
    """
    role = auth.WRITE_LEAVE_DAYS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.delete_leave_days(body)
    return AUTH_ERRORS[hasRole](role)


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
    return impl.find_leave_days_by(employee_id, start_date, end_date, year)


def find_leave_days_by_date(employeeId, leave_date):  # noqa: E501
    """Finds unique LeaveDays by employee and leave date

     # noqa: E501

    :param employeeId: Employee id to filter by
    :type employeeId: int
    :param leave_date: Leave date to filter by
    :type leave_date: str

    :rtype: LeaveDays
    """
    return impl.find_leave_days_by_date(employeeId, leave_date)


def get_leave_days_by_id(id):  # noqa: E501
    """Find LeaveDays by ID

    Returns a single LeaveDays. # noqa: E501

    :param id: ID of LeaveDays to return
    :type id: int

    :rtype: LeaveDays
    """
    return impl.get_leave_days_by_id(id)


def update_leave_days_by_id(id, body):  # noqa: E501
    """Updates a LeaveDays in the system with form data. Role write:leave_days must be granted

     # noqa: E501

    :param id: ID of LeaveDays to return
    :type id: int
    :param body: LeaveDays object that needs to be updated in the system
    :type body: dict | bytes

    :rtype: LeaveDays
    """
    role = auth.WRITE_LEAVE_DAYS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.update_leave_days_by_id(id, body)
    return AUTH_ERRORS[hasRole](role)
