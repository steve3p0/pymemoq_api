from typing import Tuple, Optional
import logging

from src import memoq_soap as mq

logging.basicConfig(level=logging.DEBUG)


class MemoqTm:
    """ A class to interact with Translation Memory objects using memoq's web service API. """

    def __init__(self, soap_client: mq.MemoqSoap) -> None:
        """ Initialize the MemoqTm class with a MemoqSoap object.
        :param soap_client: SOAP client that will make calls to the CAT tool's API
        >>> soap = mq.MemoqSoap(wsdl_base_url="some_url", api_key="some_key")
        >>> tm_client = MemoqTm(soap)
        >>> isinstance(tm_client.soap_client, mq.MemoqSoap)
        True
        """
        self.soap_client = soap_client
        self.service = 'ITMService'

    def list_tms(self) -> Tuple[int, Optional[str]]:
        """ Get the list of TMs from the memoQ Server.
        :return: status code and response content
        """
        route = '/memoqservices/tm/TMService'
        response_status, data = self.soap_client.make_soap_request(route=route, interface='ITMService', memoq_type='TMInfo', action='ListTMs')
        return response_status, data

    def list_tbs(self) -> Tuple[int, Optional[str]]:
        """ Get the list of term bases from the memoQ Server.
        :return: status code and response content
        """
        route = '/memoqservices/tb/TBService'
        response_status, data = self.soap_client.make_soap_request(route=route, interface='ITBService', memoq_type='TBInfo', action='ListTBs')
        return response_status, data


if __name__ == "__main__":
    import doctest
    doctest.testmod()
