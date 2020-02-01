import six

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
import swagger_server.controllers.team_controller_impl as impl
from swagger_server import auth, util
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.team import Team  # noqa: E501

AUTH_ERRORS = {
    auth.TokenStatus.EXPIRED: lambda role: ErrorApiResponse.TokenExpiredError(type='team'),
    auth.TokenStatus.INVALID: lambda role: ErrorApiResponse.TokenInvalidError(type='team'),
    auth.TokenStatus.NO_ROLE_GRANTED: lambda role: ErrorApiResponse.NoRoleGrantedError(role=role, type='team'),
    auth.TokenStatus.ROLE_GRANTED: None
}


def add_team(body):  # noqa: E501
    """Add a new team to the system. Role write:teams must be granted

     # noqa: E501

    :param body: Team object that needs to be added to the system
    :type body: dict | bytes

    :rtype: Team
    """
    role = auth.WRITE_TEAMS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.add_team(body)
    return AUTH_ERRORS[hasRole](role)


def delete_team(teamId):  # noqa: E501
    """Deletes an team. Role write:teams must be granteds

     # noqa: E501

    :param teamId: Team id to delete
    :type teamId: int

    :rtype: ApiResponse
    """
    role = auth.WRITE_TEAMS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.delete_team(teamId)
    return AUTH_ERRORS[hasRole](role)


def find_team_by(name):  # noqa: E501
    """Finds Teams by given parameters

     # noqa: E501

    :param name: Team name template to filter by
    :type name: str

    :rtype: List[Team]
    """
    return impl.find_team_by(name)


def find_team_by_name(name):  # noqa: E501
    """Finds Team by name

     # noqa: E501

    :param name: Team name to find
    :type name: str

    :rtype: Team
    """
    return impl.find_team_by_name(name)


def get_team_by_id(teamId):  # noqa: E501
    """Find team by ID

    Returns a single team. # noqa: E501

    :param teamId: ID of team to return
    :type teamId: int

    :rtype: Team
    """
    return impl.get_team_by_id(teamId)


def update_team_by_id(teamId, body):  # noqa: E501
    """Updates a team in the system with form data. Role write:teams must be granted

     # noqa: E501

    :param teamId: ID of team to return
    :type teamId: int
    :param body: Team object that needs to be updated in the system
    :type body: dict | bytes

    :rtype: Team
    """
    role = auth.WRITE_TEAMS
    hasRole = auth.has_role(connexion.request.headers, role)
    if hasRole == auth.TokenStatus.ROLE_GRANTED:
        return impl.update_team_by_id(teamId, body)
    return AUTH_ERRORS[hasRole](role)
