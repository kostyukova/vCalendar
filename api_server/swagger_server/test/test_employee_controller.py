# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.employee import Employee  # noqa: E501
from swagger_server.test import BaseTestCase


class TestEmployeeController(BaseTestCase):
    """EmployeeController integration test stubs"""

    def test_add_employee(self):
        """Test case for add_employee

        Add a new employee to the system. Role write:employees must be granted
        """
        body = Employee()
        response = self.client.open(
            '/vcalendar/employee',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_employee(self):
        """Test case for delete_employee

        Deletes an employee. Role write:employees must be granteds
        """
        response = self.client.open(
            '/vcalendar/employee/{employeeId}'.format(employeeId=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_all_employee(self):
        """Test case for find_all_employee

        Returns all Employees registered in the system.
        """
        response = self.client.open(
            '/vcalendar/employee/findAll',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_employee_by_email(self):
        """Test case for find_employee_by_email

        Finds Employee by given email
        """
        response = self.client.open(
            '/vcalendar/employee/findByEmail/{email}'.format(email='email_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_employees_by(self):
        """Test case for find_employees_by

        Finds Employees by given parameters
        """
        query_string = [('full_name', 'full_name_example'),
                        ('position', 'position_example'),
                        ('specialization', 'specialization_example'),
                        ('expert', true),
                        ('team_id', 56),
                        ('email', 'email_example')]
        response = self.client.open(
            '/vcalendar/employee/findBy',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_employee_by_id(self):
        """Test case for get_employee_by_id

        Find employee by ID
        """
        response = self.client.open(
            '/vcalendar/employee/{employeeId}'.format(employeeId=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_employee_by_id(self):
        """Test case for update_employee_by_id

        Updates an employee in the system with form data. Role write:employees must be granted
        """
        body = Employee()
        response = self.client.open(
            '/vcalendar/employee/{employeeId}'.format(employeeId=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
