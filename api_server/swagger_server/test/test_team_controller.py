# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.team import Team  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTeamController(BaseTestCase):
    """TeamController integration test stubs"""

    def test_add_team(self):
        """Test case for add_team

        Add a new team to the system. Role write:teams must be granted
        """
        body = Team()
        response = self.client.open(
            '/vcalendar/team',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_team(self):
        """Test case for delete_team

        Deletes an team. Role write:teams must be granteds
        """
        response = self.client.open(
            '/vcalendar/team/{teamId}'.format(teamId=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_all_team(self):
        """Test case for find_all_team

        Returns all Teams registered in the system.
        """
        response = self.client.open(
            '/vcalendar/team/findAll',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_team_by(self):
        """Test case for find_team_by

        Finds Teams by given parameters
        """
        query_string = [('name', 'name_example')]
        response = self.client.open(
            '/vcalendar/team/findBy',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_team_by_id(self):
        """Test case for get_team_by_id

        Find team by ID
        """
        response = self.client.open(
            '/vcalendar/team/{teamId}'.format(teamId=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_team_by_id(self):
        """Test case for update_team_by_id

        Updates a team in the system with form data. Role write:teams must be granted
        """
        body = Team()
        response = self.client.open(
            '/vcalendar/team/{teamId}'.format(teamId=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
