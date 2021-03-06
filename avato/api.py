import requests
from enum import Enum

AVATO_API_PREFIX = "/api"
AVATO_GENERAL_INFIX = ""
AVATO_ACTIVE_INSTANCE_INFIX = "/instance/:instanceId"


class Endpoints(str, Enum):
    GET_INSTANCES = AVATO_GENERAL_INFIX + "/instances"
    POST_CREATE_INSTANCE = AVATO_GENERAL_INFIX + "/instance"
    HEAD_USERS_EMAIL = AVATO_GENERAL_INFIX + "/users/email/:email"
    POST_RESET = AVATO_GENERAL_INFIX + "/reset"

    # Active instance shared
    GET_INFO = AVATO_ACTIVE_INSTANCE_INFIX + "/"
    GET_FATQUOTE = AVATO_ACTIVE_INSTANCE_INFIX + "/fatquote"
    POST_SHUTDOWN = AVATO_ACTIVE_INSTANCE_INFIX + "/shutdown"
    DELETE_INSTANCE = AVATO_ACTIVE_INSTANCE_INFIX + "/"
    POST_MESSAGE = AVATO_ACTIVE_INSTANCE_INFIX + "/message"


class APIError(Exception):
    def __init__(self, body):
        self.body = body

class AuthorizationError(APIError):
    """ """

    pass


class NotFoundError(APIError):
    """ """

    pass


class BadRequestError(APIError):
    """ """

    pass


class ServerError(APIError):
    """ """

    pass


class UnknownError(APIError):
    """ """

    pass


class API:
    def __init__(
        self,
        authorization_token,
        backend_host,
        backend_port,
        use_ssl,
        http_proxy,
        https_proxy,
    ):
        session = requests.Session()
        if use_ssl:
            if https_proxy:
                session.proxies = {"https": https_proxy}
            protocol = "https"
        else:
            if http_proxy:
                session.proxies = {"http": http_proxy}
            protocol = "http"
        self.base_url = f"{protocol}://{backend_host}:{backend_port}{AVATO_API_PREFIX}"
        auth_header = {"Authorization": "Bearer " + authorization_token}
        session.headers.update(auth_header)
        self.session = session

    @staticmethod
    def __check_response_status_code(response):
        if response.status_code >= 200 and response.status_code <= 204:
            pass
        elif response.status_code == 403:
            raise AuthorizationError(response.content)
        elif response.status_code == 404:
            raise NotFoundError(response.content)
        elif response.status_code == 400:
            raise BadRequestError(response.content)
        elif response.status_code == 500:
            raise ServerError(response.content)
        else:
            raise UnknownError(response.content)

    def post(self, endpoint, req_body=None, headers={}):
        url = self.base_url + endpoint
        response = self.session.post(url, data=req_body, headers={**headers})
        API.__check_response_status_code(response)
        return response

    def get(self, endpoint, headers={}):
        url = self.base_url + endpoint
        response = self.session.get(url, headers={**headers})
        API.__check_response_status_code(response)
        return response

    def head(self, endpoint, headers={}):
        url = self.base_url + endpoint
        response = self.session.head(url, headers={**headers})
        API.__check_response_status_code(response)
        return response

    def delete(self, endpoint, headers={}):
        url = self.base_url + endpoint
        response = self.session.delete(url, headers={**headers})
        API.__check_response_status_code(response)
        return response
