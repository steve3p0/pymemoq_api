import unittest
from unittest.mock import Mock

from src import memoq_soap as mq, memoq_tm as tm


class TestMemoqTm(unittest.TestCase):

    def setUp(self):
        self.soap_client = Mock(spec=mq.MemoqSoap)
        self.tm_client = tm.MemoqTm(self.soap_client)

    def test_init(self):
        self.assertIsInstance(self.tm_client.soap_client, mq.MemoqSoap)

    def test_list_tms(self):
        # Mock the make_soap_request method to return a tuple (200, "some_data")
        self.soap_client.make_soap_request.return_value = (200, "some_data")

        status, data = self.tm_client.list_tms()

        self.assertEqual(status, 200)
        self.assertEqual(data, "some_data")


if __name__ == '__main__':
    unittest.main()
