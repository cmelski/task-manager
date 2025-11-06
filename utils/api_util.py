import json
import os
import requests

from tests.conftest import logger

orders_payload = {
    "orders": [
        {
            "country": "Canada",
            "productOrderedId": "67a8df56c0d3e6622a297ccd"
        }
    ]
}


class APIBase:

    def __init__(self, url_start):

        self.base_url = url_start

    def get(self, endpoint=None, params=None, headers=None, data=None, ):
        response = requests.get(url=self.base_url + endpoint, params=params)
        logger.info(f'{self.base_url + endpoint}')
        response.raise_for_status()
        assert response.ok
        user_lists = response.json()
        logger.info(f'User Lists from API Call: {user_lists}')
        return user_lists

    def post(self, endpoint=None, data=None, params=None):
        # headers = {'Content-Type': 'application/json'}
        logger.info(f'Params: {params}')
        response = requests.post(url=self.base_url + endpoint, json=data, params=params)
        logger.info(f'{self.base_url + endpoint}')
        response.raise_for_status()
        assert response.ok
        response_message = response.json()
        logger.info(f'Response from API: {response_message}')
        return response_message
