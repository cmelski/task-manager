from tests.conftest import logger
from utils.api_util import APIBase



class APIHelper:

    def get_user_lists(self, endpoint='api/get_user_lists', params=None):
        api_base = APIBase()
        response = api_base.get(endpoint, params)
        return response

    def add_list(self, endpoint='api/add_new_list', data=None):
        api_base = APIBase()
        logger.info(f'Helper data: {data}')
        response = api_base.post(endpoint, data)
        return response

    def login(self, endpoint='api/login', data=None):
        api_base = APIBase()
        logger.info(f'Helper data: {data}')
        response = api_base.post(endpoint, data)
        return response
