# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.api_response_conflict import ApiResponseConflict  # noqa: E501
from swagger_server.models.leave_days import LeaveDays  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLeaveDaysController(BaseTestCase):
    """LeaveDaysController integration test stubs"""

    def test_add_leave_days(self):
        """Test case for add_leave_days

        Add a employee LeaveDays to the system. Role write:leave_days must be granted
        """
        body = LeaveDays()
        response = self.client.open(
            '/vcalendar/employee/leave_days',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_leave_days(self):
        """Test case for delete_leave_days

        Deletes a LeaveDays. Role write:leave_days must be granteds
        """
        response = self.client.open(
            '/vcalendar/employee/leave_days/{id}'.format(id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_employee_leave_days(self):
        """Test case for find_employee_leave_days

        Finds LeaveDays by employee
        """
        response = self.client.open(
            '/vcalendar/employee/{employeeId}/leave_days/'.format(employeeId=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_leave_days_by(self):
        """Test case for find_leave_days_by

        Finds LeaveDays by given parameters
        """
        query_string = [('employee_id', 56),
                        ('start_date', '2013-10-20'),
                        ('end_date', '2013-10-20'),
                        ('year', 56)]
        response = self.client.open(
            '/vcalendar/employee/leave_days/findBy',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_leave_days_by_date(self):
        """Test case for find_leave_days_by_date

        Finds unique LeaveDays by employee and leave date
        """
        response = self.client.open(
            '/vcalendar/employee/{employeeId}/leave_days/{leave_date}'.format(employeeId=56, leave_date='2013-10-20'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_leave_days_by_id(self):
        """Test case for get_leave_days_by_id

        Find LeaveDays by ID
        """
        response = self.client.open(
            '/vcalendar/employee/leave_days/{id}'.format(id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_leave_days_by_id(self):
        """Test case for update_leave_days_by_id

        Updates a LeaveDays in the system with form data. Role write:leave_days must be granted
        """
        body = LeaveDays()
        response = self.client.open(
            '/vcalendar/employee/leave_days/{id}'.format(id=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
