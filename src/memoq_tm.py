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

    def create_tm(self, tm_name: str, source_lang: str, target_lang: str) -> Tuple[int, Optional[str]]:
        """ Create a new Translation Memory.
        :param tm_name: Name of the new TM
        :param source_lang: Source language code
        :param target_lang: Target language code
        :return: status code and response content
        """
        route = '/memoqservices/tm/TMService'
        params = {
            'tmName': tm_name,
            'sourceLangCode': source_lang,
            'targetLangCode': target_lang
        }
        response_status, data = self.soap_client.make_soap_request(route=route, interface='ITMService', memoq_type='TMInfo', action='CreateTM', params=params)
        return response_status, data

    # ... Existing methods above

    def add_next_tmx_chunk(self, guid: str, byte_data: bytes) -> Tuple[int, Optional[str]]:
        """ Add the next TMX chunk.
        :param guid: The GUID of the TM
        :param byte_data: The byte data for the next chunk
        :return: status code and response content
        """
        # Implementation here
        pass

    def add_or_update_entry(self, source: str, target: str, guid: str) -> Tuple[int, Optional[str]]:
        """ Add or update an entry in the TM.
        :param source: The source text
        :param target: The target text
        :param guid: The GUID of the TM
        :return: status code and response content
        """
        # Implementation here
        pass

    def begin_chunked_tmx_export(self, guid: str) -> Tuple[int, Optional[str]]:
        """ Begin chunked TMX export.
        :param guid: The GUID of the TM
        :return: status code and response content
        """
        # Implementation here
        pass

    def begin_chunked_tmx_import(self, guid: str) -> Tuple[int, Optional[str]]:
        """ Begin chunked TMX import.
        :param guid: The GUID of the TM
        :return: status code and response content
        """
        # Implementation here
        pass

    def concordance(self, source: str, target: str, guid: str, concordance_request: dict) -> Tuple[int, Optional[str]]:
        """ Perform a concordance search.
        :param source: The source text
        :param target: The target text
        :param guid: The GUID of the TM
        :param concordance_request: The concordance request parameters
        :return: status code and response content
        """
        # Implementation here
        pass

    def create_and_publish(self, tm_info: dict) -> Tuple[int, Optional[str]]:
        """ Create and publish a new TM.
        :param tm_info: The TM information
        :return: status code and response content
        """
        # Implementation here
        pass

    def delete_tm(self, guid: str) -> Tuple[int, Optional[str]]:
        """ Delete a TM.
        :param guid: The GUID of the TM
        :return: status code and response content
        """
        # Implementation here
        pass

    def end_chunked_tmx_export(self, guid: str) -> Tuple[int, Optional[str]]:
        """ End chunked TMX export.
        :param guid: The GUID of the TM
        :return: status code and response content
        """
        # Implementation here
        pass

    def end_chunked_tmx_import(self, guid: str) -> Tuple[int, Optional[str]]:
        """ End chunked TMX import.
        :param guid: The GUID of the TM
        :return: status code and response content
        """
        # Implementation here
        pass

    def get_next_tmx_chunk(self, guid: str) -> Tuple[int, Optional[str]]:
        """ Get the next TMX chunk.
        :param guid: The GUID of the TM
        :return: status code and response content
        """
        # Implementation here
        pass

    def get_tm_info(self, guid: str) -> Tuple[int, Optional[str]]:
        """ Get information about a TM.
        :param guid: The GUID of the TM
        :return: status code and response content
        """

        # Code	File	Line	Column
        # [System.ServiceModel.OperationContractAttribute(Action="http://kilgray.com/memoqservices/2007/ITMService/GetTMInfo",
        #  ReplyAction="http://kilgray.com/memoqservices/2007/ITMService/GetTMInfoResponse")]
        #  C:\workspace\memoq_api\mq-ws-api-v9.14\DemoClient\Service References\TMService\Reference.cs	1666	114


        route = '/memoqservices/tm/TMService'  # The SOAP route for the TM service
        response_status, data = self.soap_client.make_soap_request(
            route=route,
            interface='ITMService',  # The interface for the TM service
            memoq_type='TMInfo',  # The type of data you're expecting
            action='GetTMInfo',  # The SOAP action you're calling
            guid=guid  # The GUID of the TM you're querying
        )
        return response_status, data

    def import_tm_metadata_scheme_from_xml(self, guid: str, xml_string: str) -> Tuple[int, Optional[str]]:
        """ Import TM metadata scheme from XML.
        :param guid: The GUID of the TM
        :param xml_string: The XML string containing the metadata scheme
        :return: status code and response content
        """
        # Implementation here
        pass

    def list_tms2(self, tm_list_filter: dict) -> Tuple[int, Optional[str]]:
        """ List TMs with a filter.
        :param tm_list_filter: The filter for listing TMs
        :return: status code and response content
        """
        # Implementation here
        pass

    def lookup_segment(self, source: str, target: str, guid: str, lookup_segment_request: dict) -> Tuple[int, Optional[str]]:
        """ Lookup a segment in the TM.
        :param source: The source text
        :param target: The target text
        :param guid: The GUID of the TM
        :param lookup_segment_request: The lookup segment request parameters
        :return: status code and response content
        """
        # Implementation here
        pass

    def start_tm_repair(self, guid: str) -> Tuple[int, Optional[str]]:
        """ Start repairing a TM.
        :param guid: The GUID of the TM
        :return: status code and response content
        """
        # Implementation here
        pass

    def update_properties(self, tm_update_info: dict) -> Tuple[int, Optional[str]]:
        """ Update TM properties.
        :param tm_update_info: The TM update information
        :return: status code and response content
        """
        # Implementation here
        pass

    # ... More methods can be added if needed


if __name__ == "__main__":
    import doctest
    doctest.testmod()
