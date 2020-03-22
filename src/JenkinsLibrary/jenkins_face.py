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

    def get_job(self, name=None):
        req = self._session.prepare_request(
            requests.Request(
                'GET',
                self._job_url(GET_JOB, name)
            )
        )
        return self._get_response(
            self._send(req)
        )

    def _send(self, req):
        return self._session.send(req, **self._settings)

    @staticmethod
    def _get_response(response):
        response.raise_for_status()
        return json.loads(response.content, encoding='utf-8')

    def _job_url(self, url_format, job_name):
        url = url_format.format(job_name)
        return self._endpoint + url
