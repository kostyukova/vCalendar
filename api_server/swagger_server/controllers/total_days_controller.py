import six

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
import swagger_server.controllers.total_days_controller_impl as impl
from swagger_server import auth, util
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.total_days import TotalDays  # noqa: E501

AUTH_ERRORS = {
    auth.TokenStatus.EXPIRED: lambda role: ErrorApiResponse.TokenExpiredError(type='Total days'),
    auth.TokenStatus.INVALID: lambda role: ErrorApiResponse.TokenInvalidError(type='Total days'),
    auth.TokenStatus.NO_ROLE_GRANTED: lambda role: ErrorApiResponse.NoRoleGrantedError(role=role, type='Total days'),
    auth.TokenStatus.ROLE_GRANTED: None
}


def add_total_days(body):  # noqa: E501
    """Add a employee total days to the system. Role write:total_days must be granted

     # noqa: E501

    :param body: TotalDays object that needs to be added to the system
    :type body: dict | bytes

    :rtype: TotalDays
    """
    role = auth.WRITE_TOTAL_DAYS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.add_total_days(id)
    return AUTH_ERRORS[hasRole](role)


def delete_total_days(id):  # noqa: E501
    """Deletes a TotalDays. Role write:total_days must be granteds

     # noqa: E501

    :param id: TotalDays id to delete
    :type id: int

    :rtype: ApiResponse
    """
    role = auth.WRITE_TOTAL_DAYS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.delete_total_days(id)
    return AUTH_ERRORS[hasRole](role)


def find_total_days_by(employee_id=None, year=None):  # noqa: E501
    """Finds TotalDays by given parameters

     # noqa: E501

    :param employee_id: Employee id to filter by
    :type employee_id: int
    :param year: Year to filter by
    :type year: int

    :rtype: List[TotalDays]
    """
    return impl.find_total_days_by(employee_id, year)


def find_total_days_by_year(employeeId, year):  # noqa: E501
    """Finds unique TotalDay by employee and year

     # noqa: E501

    :param employeeId: Employee id to filter by
    :type employeeId: int
    :param year: Year to filter by
    :type year: int

    :rtype: TotalDays
    """
    return impl.find_total_days_by_year(employeeId, year)


def get_total_days_by_id(id):  # noqa: E501
    """Find total days by ID

    Returns a single TotalDays. # noqa: E501

    :param id: ID of TotalDays to return
    :type id: int

    :rtype: TotalDays
    """
    return impl.get_total_days_by_id(id)


def update_total_days_by_id(id, body):  # noqa: E501
    """Updates a TotalDays in the system with form data. Role write:total_days must be granted

     # noqa: E501

    :param id: ID of TotalDays to return
    :type id: int
    :param body: TotalDays object that needs to be updated in the system
    :type body: dict | bytes

    :rtype: TotalDays
    """
    role = auth.WRITE_TOTAL_DAYS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.update_total_days_by_id(id, body)
    return AUTH_ERRORS[hasRole](role)
