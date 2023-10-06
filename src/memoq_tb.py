from typing import Tuple, Optional
import logging

from src import memoq_soap as mq

logging.basicConfig(level=logging.DEBUG)


class MemoqTb:
    """ A class to interact with Term Base objects using memoq's web service API. """

    def __init__(self, soap_client: mq.MemoqSoap) -> None:
        """ Initialize the MemoqTb class with a MemoqSoap object.
        :param soap_client: SOAP client that will make calls to the CAT tool's API
        >>> soap = mq.MemoqSoap(wsdl_base_url="some_url", api_key="some_key")
        >>> tb_client = MemoqTb(soap)
        >>> isinstance(tb_client.soap_client, mq.MemoqSoap)
        True
        """
        self.soap_client = soap_client
        self.service = 'ITBService'

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
