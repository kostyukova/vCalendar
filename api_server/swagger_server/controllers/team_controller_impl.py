import six

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
from swagger_server import db, util
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.team import Team  # noqa: E501
from swagger_server.orm import Team as Team_orm


def add_team(body):  # noqa: E501
    """Add a new team to the system. Role write:teams must be granted

     # noqa: E501

    :param body: Team object that needs to be added to the system
    :type body: dict | bytes

    :rtype: Team
    """
    if connexion.request.is_json:
        body = Team.from_dict(connexion.request.get_json())  # noqa: E501
    # check team already exists by name
    found = Team_orm.query.filter_by(name=body.name).one_or_none()
    if found is not None:
        return ErrorApiResponse.TeamExistError(body.name), 409
    try:
        db.session.add(Team_orm(name=body.name))
        db.session.commit()
        return find_team_by_name(body.name)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='team'), 500


def delete_team(teamId):  # noqa: E501
    """Deletes an team. Role write:teams must be granteds

     # noqa: E501

    :param teamId: Team id to delete
    :type teamId: int

    :rtype: ApiResponse
    """
    found = Team_orm.query.get(teamId)
    if found is None:
        return ErrorApiResponse.TeamNotFoundError(id=teamId), 404
    try:
        db.session.delete(found)
        db.session.commit()
        return 'Successful operation', 204
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='team'), 500


def find_all_team():  # noqa: E501
    """Returns all Teams registered in the system.

     # noqa: E501


    :rtype: List[Team]
    """
    found = Team_orm.query.all()
    return [to_team_dto(elem) for elem in found]


def find_team_by(name=None):  # noqa: E501
    """Finds Teams by given parameters

     # noqa: E501

    :param name: Team name template to filter by
    :type name: str

    :rtype: List[Team]
    """
    query = Team_orm.query
    if name and name.strip():
        query = query.filter(Team_orm.name.ilike(
            '%' + name.strip() + '%'))
    try:
        return [to_team_dto(elem) for elem in query.all()]
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='team'), 500


def find_team_by_name(name):  # noqa: E501
    """Finds Team by name

     # noqa: E501

    :param name: Team name to find
    :type name: str

    :rtype: Team
    """
    found = Team_orm.query.filter_by(name=name).one_or_none()
    if found is None:
        return ErrorApiResponse.TeamNotFoundError(name=name), 404
    return to_team_dto(found)


def get_team_by_id(teamId):  # noqa: E501
    """Find team by ID

    Returns a single team. # noqa: E501

    :param teamId: ID of team to return
    :type teamId: int

    :rtype: Team
    """
    found = Team_orm.query.get(teamId)
    if found is None:
        return ErrorApiResponse.TeamNotFoundError(id=teamId), 404
    return to_team_dto(found)


def update_team_by_id(teamId, body):  # noqa: E501
    """Updates a team in the system with form data. Role write:teams must be granted

     # noqa: E501

    :param teamId: ID of team to return
    :type teamId: int
    :param body: Team object that needs to be updated in the system
    :type body: dict | bytes

    :rtype: Team
    """
    found = Team_orm.query.get(teamId)
    if found is None:
        return ErrorApiResponse.TeamNotFoundError(id=teamId), 404
    if connexion.request.is_json:
        body = Team.from_dict(connexion.request.get_json())  # noqa: E501
    # check team already exists by name
    duplicate = Team_orm.query.filter_by(name=body.name).one_or_none()
    if duplicate is not None:
        return ErrorApiResponse.TeamExistError(body.name), 409
    found.name = body.name
    try:
        db.session.add(found)
        db.session.commit()
        return get_team_by_id(teamId)
    except Exception as ex:
        return ErrorApiResponse.InternalServerError(ex, type='team'), 500


def to_team_dto(found: Team_orm):
    return Team(team_id=found.team_id, name=found.name)
