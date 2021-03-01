#!/usr/bin/python3

# sparql_adapter.py
# Date:  20/12/2020
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com

"""
Adapter for the SPARQL wrapper library
"""
import logging
from abc import ABC, abstractmethod
from json import JSONDecodeError
from urllib.parse import urljoin

from requests.auth import HTTPBasicAuth
from requests_toolbelt import MultipartEncoder

from lam4doc.adapters.helpers import get_file_format
from lam4doc.config import config

logger = logging.getLogger(config.LAM_LOGGER)


class FusekiException(Exception):
    """
        An exception when Fuseki server interaction has failed.
    """


class AbstractSPARQLAdapter(ABC):
    """
    Abstract adapter for performing operations on a triple store server
    """

    @abstractmethod
    def create_dataset(self, dataset_name: str):
        """
        :param dataset_name: the name of the target dataset
        """

    @abstractmethod
    def delete_graph(self, dataset_name: str, graph_name: str):
        """
        :param dataset_name: the name of the target dataset
        :param graph_name: the name of the graph to be deleted
        """

    @abstractmethod
    def upload_file_to_graph(self, dataset_name: str, graph_name: str, file_path: str):
        """
            Upload a data file to the dataset
        :param dataset_name: The dataset identifier. This should be short alphanumeric string uniquely
        :param file_path: path to the data file to be uploaded
        :param graph_name: the name of the target graph
        """


class FusekiSPARQLAdapter(AbstractSPARQLAdapter):
    def create_dataset(self, dataset_name: str):
        logger.debug('Attempting to create dataset named ' + dataset_name)

        response = self.http_client.post(
            url=urljoin(self.triplestore_service_url, "/$/datasets?dbName=" + dataset_name + "&dbType=tdb"),
            auth=HTTPBasicAuth(config.LAM_FUSEKI_USERNAME,
                               config.LAM_FUSEKI_PASSWORD))
        logger.debug(response.text)
        if response.status_code != 200:
            raise FusekiException(f'Error while attempting to create the specified dataset: {response.text}')

        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    def __init__(self, triplestore_service_url: str, http_client):
        self.triplestore_service_url = triplestore_service_url
        self.http_client = http_client

    def delete_graph(self, dataset_name: str, graph_name: str) -> bool:
        query_data = {"update": "DROP GRAPH " + f"<{graph_name}>"}
        logger.debug("QUERY DATA = " + str(query_data))

        response = self.http_client.post(url=urljoin(self.triplestore_service_url, f"/{dataset_name}/update"),
                                         auth=HTTPBasicAuth(config.LAM_FUSEKI_USERNAME,
                                                            config.LAM_FUSEKI_PASSWORD),
                                         data=query_data)
        logger.debug(response.text)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            raise FusekiException(f'Error while attempting to delete the graph: {response.text}')

    def upload_file_to_graph(self, dataset_name: str, graph_name: str, file_path: str) -> dict:
        """
            Upload the file to a Fuseki dataset into a specific graph
        :param dataset_name: The dataset identifier. This should be short alphanumeric string uniquely
        :param graph_name: the name of the target graph
        :param file_path: path to the data file to be uploaded
        :return a dict of the structure:
        {
          "count": 36286,
          "tripleCount": 36286,
          "quadCount": 0
        }
        """
        # as mentioned in the official requests documentation
        # https://requests.readthedocs.io/en/master/user/quickstart/#post-a-multipart-encoded-file
        # for larger requests, it has to be streamed, which requests doesn't support by default.
        # requests_toolbelt solution - https://toolbelt.readthedocs.io/en/latest/uploading-data.html
        multipart_encoder = MultipartEncoder(
            fields={'file': (file_path, open(file_path, 'rb'), get_file_format(file_path))}
        )

        response = self.http_client.post(
            urljoin(self.triplestore_service_url, f"/{dataset_name}/data?graph=" + graph_name),
            data=multipart_encoder,
            auth=HTTPBasicAuth(config.LAM_FUSEKI_USERNAME,
                               config.LAM_FUSEKI_PASSWORD),
            headers={'Content-Type': multipart_encoder.content_type})

        if response.status_code == 201:
            logger.debug(
                "Successfully uploaded the file '" + file_path + "' into the graph '" + graph_name + "' of the dataset '" + dataset_name + "'")

        if response.status_code == 200:
            logger.warning("The triple store responded with HTTP status code 200 OK ! This means you ADDED "
                           "data into an existing graph instead of uploading it to a new one !")

        if response.status_code != 200 and response.status_code != 201:
            raise FusekiException("Error uploading file to graph: " + response.text)

        try:
            return response.json()
        except JSONDecodeError:
            return response.text
