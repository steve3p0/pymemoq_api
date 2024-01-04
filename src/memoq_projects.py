from typing import Tuple, Optional
import logging

from src import memoq_soap as mq

logging.basicConfig(level=logging.DEBUG)


class MemoqProjects:
    """ A class to interact with Project objects using memoq's web service API. """

    def __init__(self, soap_client: mq.MemoqSoap) -> None:
        """ Initialize the MemoqProjects class with a MemoqSoap object.
        :param soap_client: SOAP client that will make calls to the CAT tool's API
        >>> soap = mq.MemoqSoap(wsdl_base_url="some_url", api_key="some_key")
        >>> project_client = MemoqProjects(soap)
        >>> isinstance(project_client.soap_client, mq.MemoqSoap)
        True
        """
        self.soap_client = soap_client
        self.service = 'IServerProjectService'

    def list_projects(self, filter: Optional[str] = None) -> Tuple[int, Optional[str]]:
        """ Get the list of projects from the memoQ Server.
        :param filter: Optional filter to apply when listing projects
        :return: status code and response content
        """

        route = 'memoqservices/ServerProject/ServerProjectService'

        if filter is None:
            response_status, data = self.soap_client.make_soap_request(
                route=route,
                interface='IServerProjectService',
                memoq_type='ServerProjectInfo',
                action='ListProjects'
            )
        else:
            response_status, data = self.soap_client.make_soap_request(
                route=route,
                interface='IServerProjectService',
                memoq_type='ServerProjectInfo',
                action='ListProjects',
                additional_params={'filter': filter} if filter else None
            )

        return response_status, data

    def list_project_translation_documents(self, guid: str) -> Tuple[int, Optional[str]]:
        """ List the translation documents in a project.
        :param guid: The GUID of the project
        :return: status code and response content
        """
        # route = '/memoqservices/project/ProjectService'
        route = 'memoqservices/ServerProject/ServerProjectService'
        action = 'ListProjectTranslationDocuments'

        # Construct the payload body based on the provided guid and options
        # payload_body = f'''
        #     <ListProjectTranslationDocuments2 xmlns="{self.soap_client._namespace}">
        #         <guid>{guid}</guid>
        #         <options>
        #             <!-- Add options here based on the 'options' dict -->
        #         </options>
        #     </ListProjectTranslationDocuments2>
        # '''

        # payload_body = f'''
        #     <ListProjectTranslationDocuments2 xmlns="{self.soap_client._namespace}">
        #         <guid>{guid}</guid>
        #     </ListProjectTranslationDocuments2>
        # '''

        # guid = f'<guid>{guid}</guid>'

        response_status, data = self.soap_client.make_soap_request(
            route=route,
            interface='IServerProjectService',
            memoq_type='ServerProjectTranslationDocument',
            action=action,
            # serverProjectGuid=guid
            guid=guid  # Pass the constructed payload_body
        )

        return response_status, data

    def list_project_translation_documents2(self, guid: str, options: dict = None) -> Tuple[int, Optional[str]]:
        """ List the translation documents in a project.
        :param guid: The GUID of the project
        :param options: Additional options for listing documents
        :return: status code and response content
        """
        # route = '/memoqservices/project/ProjectService'
        route = 'memoqservices/ServerProject/ServerProjectService'
        action = 'ListProjectTranslationDocuments2'

        # Construct the payload body based on the provided guid and options
        # payload_body = f'''
        #     <ListProjectTranslationDocuments2 xmlns="{self.soap_client._namespace}">
        #         <guid>{guid}</guid>
        #         <options>
        #             <!-- Add options here based on the 'options' dict -->
        #         </options>
        #     </ListProjectTranslationDocuments2>
        # '''

        # payload_body = f'''
        #     <ListProjectTranslationDocuments2 xmlns="{self.soap_client._namespace}">
        #         <guid>{guid}</guid>
        #     </ListProjectTranslationDocuments2>
        # '''

        # guid = f'<guid>{guid}</guid>'

        response_status, data = self.soap_client.make_soap_request(
            route=route,
            interface='IServerProjectService',
            memoq_type='ServerProjectTranslationDocument2',
            action=action,
            # serverProjectGuid=guid
            guid=guid  # Pass the constructed payload_body
        )

        return response_status, data



if __name__ == "__main__":
    import doctest
    doctest.testmod()
