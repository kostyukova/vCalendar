# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class UserSafe(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, id: int=None, username: str=None, email: str=None, password: str=None, roles: str=None):  # noqa: E501
        """UserSafe - a model defined in Swagger

        :param id: The id of this UserSafe.  # noqa: E501
        :type id: int
        :param username: The username of this UserSafe.  # noqa: E501
        :type username: str
        :param email: The email of this UserSafe.  # noqa: E501
        :type email: str
        :param password: The password of this UserSafe.  # noqa: E501
        :type password: str
        :param roles: The roles of this UserSafe.  # noqa: E501
        :type roles: str
        """
        self.swagger_types = {
            'id': int,
            'username': str,
            'email': str,
            'password': str,
            'roles': str
        }

        self.attribute_map = {
            'id': 'id',
            'username': 'username',
            'email': 'email',
            'password': 'password',
            'roles': 'roles'
        }

        self._id = id
        self._username = username
        self._email = email
        self._password = password
        self._roles = roles

    @classmethod
    def from_dict(cls, dikt) -> 'UserSafe':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserSafe of this UserSafe.  # noqa: E501
        :rtype: UserSafe
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this UserSafe.


        :return: The id of this UserSafe.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this UserSafe.


        :param id: The id of this UserSafe.
        :type id: int
        """

        self._id = id

    @property
    def username(self) -> str:
        """Gets the username of this UserSafe.


        :return: The username of this UserSafe.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username: str):
        """Sets the username of this UserSafe.


        :param username: The username of this UserSafe.
        :type username: str
        """
        if username is None:
            raise ValueError("Invalid value for `username`, must not be `None`")  # noqa: E501

        self._username = username

    @property
    def email(self) -> str:
        """Gets the email of this UserSafe.


        :return: The email of this UserSafe.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this UserSafe.


        :param email: The email of this UserSafe.
        :type email: str
        """
        if email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def password(self) -> str:
        """Gets the password of this UserSafe.


        :return: The password of this UserSafe.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this UserSafe.


        :param password: The password of this UserSafe.
        :type password: str
        """

        self._password = password

    @property
    def roles(self) -> str:
        """Gets the roles of this UserSafe.


        :return: The roles of this UserSafe.
        :rtype: str
        """
        return self._roles

    @roles.setter
    def roles(self, roles: str):
        """Sets the roles of this UserSafe.


        :param roles: The roles of this UserSafe.
        :type roles: str
        """

        self._roles = roles