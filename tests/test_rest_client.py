import unittest
from requests import Response
from unittest.mock import MagicMock

from pysqldbm.rest_client import RestClient


class SessionWithUrlBaseTests:
    def test_request_prepends_base_url(self):
        # Arrange
        url_base = "https://api.example.com"
        url = "/resource"
        expected_url = "https://api.example.com/resource"
        session = RestClient.SessionWithUrlBase(url_base=url_base)

        # Act
        response = session.request("GET", url)

        # Assert
        self.assertEqual(response.url, expected_url)

    def test_request_calls_super_request(self):
        # Arrange
        session = RestClient.SessionWithUrlBase()
        session.request = MagicMock(return_value=Response())

        # Act
        response = session.request("GET", "https://api.example.com/resource")

        # Assert
        session.request.assert_called_once_with("GET", "https://api.example.com/resource")
        self.assertIsInstance(response, Response)
