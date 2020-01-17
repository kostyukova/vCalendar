import connexion
import six

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.team import Team  # noqa: E501
from swagger_server import util


def add_team(body):  # noqa: E501
    """Add a new team to the system. Role write:teams must be granted

     # noqa: E501

    :param body: Team object that needs to be added to the system
    :type body: dict | bytes

    :rtype: Team
    """
    if connexion.request.is_json:
        body = Team.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_team(teamId):  # noqa: E501
    """Deletes an team. Role write:teams must be granteds

     # noqa: E501

    :param teamId: Team id to delete
    :type teamId: int

    :rtype: ApiResponse
    """
    return 'do some magic!'


def find_all_team():  # noqa: E501
    """Returns all Teams registered in the system.

     # noqa: E501


    :rtype: List[Team]
    """
    return 'do some magic!'


def find_team_by(name=None):  # noqa: E501
    """Finds Teams by given parameters

     # noqa: E501

    :param name: Team name template to filter by
    :type name: str

    :rtype: List[Team]
    """
    return 'do some magic!'


def get_team_by_id(teamId):  # noqa: E501
    """Find team by ID

    Returns a single team. # noqa: E501

    :param teamId: ID of team to return
    :type teamId: int

    :rtype: Team
    """
    return 'do some magic!'


def update_team_by_id(teamId, body):  # noqa: E501
    """Updates a team in the system with form data. Role write:teams must be granted

     # noqa: E501

    :param teamId: ID of team to return
    :type teamId: int
    :param body: Team object that needs to be updated in the system
    :type body: dict | bytes

    :rtype: Team
    """
    if connexion.request.is_json:
        body = Team.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
