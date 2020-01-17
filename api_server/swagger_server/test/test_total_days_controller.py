# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.total_days import TotalDays  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTotalDaysController(BaseTestCase):
    """TotalDaysController integration test stubs"""

    def test_add_total_days(self):
        """Test case for add_total_days

        Add a employee total days to the system. Role write:total_days must be granted
        """
        body = TotalDays()
        response = self.client.open(
            '/vcalendar/employee/total_days',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_total_days(self):
        """Test case for delete_total_days

        Deletes a TotalDays. Role write:total_days must be granteds
        """
        response = self.client.open(
            '/vcalendar/employee/total_days/{id}'.format(id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_total_days_by(self):
        """Test case for find_total_days_by

        Finds TotalDays by given parameters
        """
        query_string = [('employee_id', 56),
                        ('year', 56)]
        response = self.client.open(
            '/vcalendar/employee/total_days/findBy',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_total_days_by_year(self):
        """Test case for find_total_days_by_year

        Finds unique TotalDay by employee and year
        """
        response = self.client.open(
            '/vcalendar/employee/{employeeId}/total_days/{year}'.format(employeeId=56, year=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_total_days_by_id(self):
        """Test case for get_total_days_by_id

        Find total days by ID
        """
        response = self.client.open(
            '/vcalendar/employee/total_days/{id}'.format(id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_total_days_by_id(self):
        """Test case for update_total_days_by_id

        Updates a TotalDays in the system with form data. Role write:total_days must be granted
        """
        body = TotalDays()
        response = self.client.open(
            '/vcalendar/employee/total_days/{id}'.format(id=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
