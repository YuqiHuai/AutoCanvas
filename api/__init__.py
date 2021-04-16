import requests

from utils import get_logger
from utils.config import Config


class API:
    """
    Wrapper for requests, adds access_token to every request.
    """
    __instance__ = None

    def __init__(self, config: Config):
        assert API.__instance__ is None, 'An instance is already initialized'
        self.token = config.auth_token
        self.logger = get_logger('API')
        API.__instance__ = self

    @staticmethod
    def get_instance():
        assert API.__instance__ is not None, 'No instance initialized'
        return API.__instance__

    def delete(self, url: str, params: dict = dict()):
        params['access_token'] = self.token
        response = requests.delete(url, params=params)
        return response

    def put(self, url: str, data=dict(), params=dict()):
        params['access_token'] = self.token
        response = requests.put(url, data, params=params)
        return response

    def get(self, url: str, params: dict = dict()):
        params['access_token'] = self.token
        response = requests.get(url, params=params)
        return response

    def get_paginated(self, url: str, params: dict = dict()):
        params['access_token'] = self.token
        result = list()
        while True:
            response = requests.get(url, params=params)
            result.append(response)
            if not response.links.get('next'):
                self.logger.debug('FETCH COMPLETED')
                break
            else:
                self.logger.debug('FETCH COMPLETED. HAS ANOTHER PAGE')
                url = response.links['next']['url']
                param = {'access_token': self.token}
        return result
