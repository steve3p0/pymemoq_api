import unittest
from unittest.mock import patch
import requests
from src.memoq_soap import MemoqSoap


class TestMemoqSoap(unittest.TestCase):

    def setUp(self):
        self.soap_client = MemoqSoap("some_url", "some_key")

    def test_init(self):
        self.assertEqual(self.soap_client._wsdl_base_url, "some_url")

    def test_generate_payload(self):
        template = '<template><soap:Body></soap:Body></template>'
        payload_body = '<ListTMs xmlns="some_namespace"></ListTMs>'
        result = self.soap_client.generate_payload(template, payload_body)
        expected = '<template><soap:Body><ListTMs xmlns="some_namespace"></ListTMs></soap:Body></template>'
        self.assertEqual(result, expected)

    @patch('requests.request')
    def test_make_soap_request(self, mock_request):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'<s:Envelope><s:Body><ListTMsResponse><ListTMsResult><TMInfo>list</TMInfo></ListTMsResult></ListTMsResponse></s:Body></s:Envelope>'
        mock_request.return_value = mock_response

        route = '/memoqservices/tm/TMService'
        status, data = self.soap_client.make_soap_request(route=route, interface="ITMService", memoq_type="TMInfo", action="ListTMs")
        self.assertEqual(status, 200)
        self.assertIsNotNone(data)

    def test_parse_xml_response(self):
        xml = '<s:Envelope><s:Body><ListTMsResponse><ListTMsResult><TMInfo>list</TMInfo></ListTMsResult></ListTMsResponse></s:Body></s:Envelope>'
        result = self.soap_client.parse_xml_response(xml, "TMInfo", "ListTMs")
        self.assertEqual(result, "list")

if __name__ == '__main__':
    unittest.main()
