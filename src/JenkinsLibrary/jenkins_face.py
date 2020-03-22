import requests
import urllib3
import json

BASE_ENDPOINT = '{}://{}:{}@{}/'
GET_JOB = '{}/api/json'


class JenkinsFace(object):

    def __init__(self,
                 protocol='https',
                 url=None,
                 username=None,
                 password=None,
                 verify=False):
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._endpoint = BASE_ENDPOINT.format(protocol, username, password, url)
        self._session = requests.Session()
        self._settings = self._session.merge_environment_settings(
            self._endpoint, {}, None, verify, None
        )
        self._settings['allow_redirects'] = False
