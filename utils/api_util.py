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

    def __init__(self):
        self.base_url = os.environ.get('BASE_URL')

    def get(self, endpoint=None, params=None, headers=None, data=None, ):
        response = requests.get(url=self.base_url+endpoint, params=params)
        logger.info(f'{self.base_url+endpoint}')
        response.raise_for_status()
        assert response.ok
        user_lists = response.json()
        logger.info(f'User Lists from API Call: {user_lists}')
        return user_lists

    def post(self, endpoint=None, data=None):
        #headers = {'Content-Type': 'application/json'}
        response = requests.post(url=self.base_url+endpoint, json=data)
        logger.info(f'{self.base_url+endpoint}')
        response.raise_for_status()
        assert response.ok
        add_list_response = response.json()
        logger.info(f'Add List response from API: {add_list_response}')
        return add_list_response
