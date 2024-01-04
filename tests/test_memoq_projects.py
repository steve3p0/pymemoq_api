import unittest
from unittest.mock import Mock

from src import memoq_soap as mq, memoq_projects as mp


class TestMemoqProjects(unittest.TestCase):

    def setUp(self):
        self.soap_client = Mock(spec=mq.MemoqSoap)
        self.project_client = mp.MemoqProjects(self.soap_client)

    def test_init(self):
        self.assertIsInstance(self.project_client.soap_client, mq.MemoqSoap)

    def test_list_projects(self):
        # Mock the make_soap_request method to return a tuple (200, "project_data")
        self.soap_client.make_soap_request.return_value = (200, "project_data")

        status, data = self.project_client.list_projects()

        self.assertEqual(status, 200)
        self.assertEqual(data, "project_data")

    def test_list_project_translation_documents2(self):
        # Mock the make_soap_request method to return a tuple (200, "some_data")
        self.soap_client.make_soap_request.return_value = (200, "some_data")

        guid = "some_guid"
        options = {"some_option": "some_value"}

        status, data = self.project_client.list_project_translation_documents2(guid, options)

        self.assertEqual(status, 200)
        self.assertEqual(data, "some_data")

    def test_list_projects_with_filter(self):
        # Mock the make_soap_request method to return a tuple (200, "filtered_project_data")
        self.soap_client.make_soap_request.return_value = (200, "filtered_project_data")

        status, data = self.project_client.list_projects(filter="some_filter")

        self.assertEqual(status, 200)
        self.assertEqual(data, "filtered_project_data")

    def test_list_project_translation_documents(self):
        # Mock the make_soap_request method to return a tuple (200, "some_data")
        self.soap_client.make_soap_request.return_value = (200, "some_data")

        guid = "some_guid"
        options = {"some_option": "some_value"}

        status, data = self.project_client.list_project_translation_documents(guid)

        self.assertEqual(status, 200)
        self.assertEqual(data, "some_data")

    def test_list_project_translation_documents2(self):
        # Mock the make_soap_request method to return a tuple (200, "some_data")
        self.soap_client.make_soap_request.return_value = (200, "some_data")

        guid = "some_guid"
        options = {"some_option": "some_value"}

        status, data = self.project_client.list_project_translation_documents2(guid, options)

        self.assertEqual(status, 200)
        self.assertEqual(data, "some_data")


if __name__ == '__main__':
    unittest.main()
