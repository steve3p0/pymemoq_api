from typing import Optional
import os
import configparser
import requests
import json
import xmltodict
import logging

# Debugging urllib3
import contextlib
from http.client import HTTPConnection


logging.basicConfig(level=logging.DEBUG)

def debug_requests_on():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def debug_requests_off():
    '''Switches off logging of the requests module, might be some side-effects'''
    HTTPConnection.debuglevel = 0

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False

@contextlib.contextmanager
def debug_requests():
    '''Use with 'with'!'''
    debug_requests_on()
    yield
    debug_requests_off()


class MemoqSoap:
    """ A class to interact with memoQ's Web API using SOAP. """

    def __init__(self, wsdl_base_url: str, api_key: str) -> None:
        """ Initialize the memoq SOAP class
        :param wsdl_base_url:
        :param api_key:
        >>> MemoqSoap("some_url", "some_key")._wsdl_base_url
        'some_url'
        """

        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'memoq.references.ini')
        config = configparser.ConfigParser()
        config.read(config_path)

        # Protected Attributes

        # Load the config file if the wsdl_base_url is None
        if wsdl_base_url is None:
            self._load_config()

        self._wsdl_base_url = wsdl_base_url
        self._api_key = api_key
        self._namespace = config.get('SCHEMA', 'NAMESPACE')
        self._payload_template = f"""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                <soap:Header>
                    <ApiKey xmlns="{self._namespace}">{self._api_key}</ApiKey>
                </soap:Header>
                <soap:Body></soap:Body>
            </soap:Envelope>"""

        # Public Fields
        self.headers = {'Content-Type': 'text/xml; charset=utf-8', 'SOAPAction': ''}
        self.route = None
        self.payload = None
        self.response = None
        self.response_status_code = None
        self.response_content = None
        self.response_text = None
        self.error_message = None

    def _load_config(self):
        # Construct the config file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, '..', 'memoq.config.ini')  # If memoq.config.ini is inside a config directory

        config = configparser.ConfigParser()
        config.read(config_path)
        self._wsdl_base_url = config.get('API', 'API_URL')
        self._api_key = config.get('API', 'API_KEY')

    @staticmethod
    def generate_payload(template: str, payload_body: str) -> str:
        """ Generate the SOAP payload.
        >>> mq = MemoqSoap(wsdl_base_url="some_url", api_key="some_key")
        >>> t = '<template><soap:Body></soap:Body></template>'
        >>> p = '<ListTMs xmlns="some_namespace"></ListTMs>'
        >>> mq.generate_payload(template=t, payload_body=p)
        '<template><soap:Body><ListTMs xmlns="some_namespace"></ListTMs></soap:Body></template>'
        """

        payload = template
        payload = payload.replace("<soap:Body></soap:Body>", f"<soap:Body>{payload_body}</soap:Body>")

        return payload

    def make_soap_request(self, route: str, interface: str, memoq_type: str, action: str, **kwargs) -> tuple[int, str]:
        """ Make a SOAP request to Memoq API.
        :param route: route to the service requested
        :param interface: the interface to be used
        :param memoq_type: the type of object to be retrieved
        :param action: the action to be performed
        :param kwargs: additional parameters like guid
        :return: the response from the CAT tool's API
        """

        url = f'{self._wsdl_base_url}/{route}'
        soap_action = f"{interface}/{action}"

        # Generate the payload body dynamically based on the action and additional parameters
        payload_body = f'<{action} xmlns="{self._namespace}">'

        # Build the payload body based on the additional parameters
        for key, value in kwargs.items():
            payload_body += f'<{key}>{value}</{key}>'

        payload_body += f'</{action}>'

        self.payload = self.generate_payload(self._payload_template, payload_body)
        self.headers['SOAPAction'] = f"{self._namespace}/{soap_action}"

        print(f"self._wsdl_url: {self._wsdl_base_url}")
        print(f"self.headers: {self.headers}")
        print(f"self.payload: {self.payload}")

        debug_requests_on()
        self.response = requests.request("POST", url, headers=self.headers, data=self.payload)
        debug_requests_off()

        self.response_status_code = self.response.status_code
        self.response_content = self.response.content.decode()

        if self.response.status_code != 200:
            self.error_message = f"Error: {self.response.status_code}\nHeaders: {self.response.headers}\nResponse: {self.response.text}"
            return self.response.status_code, self.error_message

        parse_xml_response = self.parse_xml_response(response_text=self.response_content, memoq_type=memoq_type, action=action)
        json_data = json.dumps(parse_xml_response, indent=4)
        return self.response_status_code, json_data

    @staticmethod
    def parse_xml_response(response_text: str, memoq_type: str, action: str = None) -> Optional[dict]:
        """ Parse the XML response from the CAT tool's API
        :param response_text: The XML response text
        :param memoq_type: The type of MemoQ object (e.g., 'TMInfo', 'TBInfo')
        :param action: The action performed (e.g., 'ListTMs', 'ListTBs')
        :return: the parsed XML response as a dictionary
        >>> xml = '<s:Envelope><s:Body><ListTMsResponse><ListTMsResult><TMInfo>list</TMInfo></ListTMsResult></ListTMsResponse></s:Body></s:Envelope>'
        >>> MemoqSoap.parse_xml_response(response_text=xml, memoq_type='TMInfo', action='ListTMs')  # Assuming a single TM object in the response
        'list'
        >>> xml = '<s:Envelope><s:Body><TMInfo>translation memory</TMInfo></s:Body></s:Envelope>'
        >>> MemoqSoap.parse_xml_response(response_text=xml, memoq_type='TMInfo')  # Assuming a single TM object in the response
        'translation memory'
        """

        parsed_xml = xmltodict.parse(response_text)

        if action is None:
            data = parsed_xml['s:Envelope']['s:Body'][memoq_type]
        elif action == 'GetTMInfo':
            action_response = f"{action}Response"
            action_result = f"{action}Result"
            data = parsed_xml['s:Envelope']['s:Body'][action_response][action_result]
        else:
            action_response = f"{action}Response"
            action_result = f"{action}Result"
            data = parsed_xml['s:Envelope']['s:Body'][action_response][action_result][memoq_type]

        return data


if __name__ == "__main__":
    import doctest
    doctest.testmod()
