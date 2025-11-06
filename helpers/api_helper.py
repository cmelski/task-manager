from tests.conftest import logger
from utils.api_util import APIBase



class APIHelper:

    def get_user_lists(self, url_start, endpoint='api/get_user_lists', params=None):
        api_base = APIBase(url_start)
        response = api_base.get(endpoint, params)
        return response

    def add_list(self, url_start, endpoint='api/add_new_list', data=None):
        api_base = APIBase(url_start)
        logger.info(f'Helper data: {data}')
        response = api_base.post(endpoint, data)
        return response

    def login(self, endpoint='api/login_test', data=None, params=None):
        api_base = APIBase()
        logger.info(f'Helper data: {data}')
        logger.info(f'Params: {params}')
        api_base.post(endpoint, data, params)

