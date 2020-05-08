import requests
import json
import urllib3
import time
from robot.api.deco import keyword
from .version import VERSION

__version__ = VERSION

BASE_ENDPOINT = '{}://{}:{}@{}/'
GET_JOB = '{}/api/json'
GET_JOB_BUILD = '{}/{}/api/json'
BUILD_JOB_WITH_PARAMETERS = '{}/buildWithParameters'


class JenkinsFace(object):

    def __init__(self):
        self._endpoint = None
        self._session = None
        self._settings = None
        self._requests = None

    @keyword('Create Session Jenkins')
    def create_session_jenkins(self,
                               protocol='https',
                               url=None,
                               username=None,
                               password=None,
                               verify=False):
        """Create Session Jenkins

        To initiate session of jenkins

        Arguments:
            - protocol: http or https ``str``
            - url: jenkins base url ``str``
            - username: username of jenkins account ``str``
            - password: password or token of jenkins account ``str``
            - verify: to ignore verifying the SSL certificate set to False ``bool``

        Return nothing

        Examples:
        | create session jenkins | ${protocol} | ${host} | ${username} | ${password} | ${verify} |
        """
        if not url or not username or not password:
            raise Exception('Require parameters should not be none')
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._endpoint = BASE_ENDPOINT.format(protocol, username, password, url)
        self._session = requests.Session()
        self._settings = self._session.merge_environment_settings(
            self._endpoint, {}, None, verify, None
        )
        self._settings['allow_redirects'] = False

    @keyword('Get Jenkins Job')
    def get_jenkins_job(self, name=None):
        """Get Jenkins Job

        Get jenkins job details

        Arguments:
            - name: fullname of job ``str``

        Return dictionary of job information ``dict``

        Examples:
        | ${job_details}= | Get Jenkins Job | ${job_full_name} |
        """
        if not name:
            raise Exception('Job name should not be None')
        req = self._session.prepare_request(
            requests.Request(
                'GET',
                self._job_url(GET_JOB, [self._job_folder(name)])
            )
        )
        return self._get_response(
            self._send(req)
        )

    @keyword('Get Jenkins Job Build')
    def get_jenkins_job_build(self, name=None, build_number='lastBuild'):
        """Get Jenkins Job Build

        Get build details of jenkins job by build number,
        And if need latest build, leave build_number blank.

        Arguments:
            - name: fullname of job ``str``
            - build_number: number of build ``str``

        Return dictionary of job information ``dict``

        Examples:
        | ${job_build_details}= | Get Jenkins Job Build | ${job_full_name} | ${build_number} |
        """
        if not name:
            raise Exception('Job name should not be None')
        req = self._session.prepare_request(
            requests.Request(
                'GET',
                self._job_url(GET_JOB_BUILD, [self._job_folder(name), build_number])
            )
        )
        self._requests = requests
        return self._get_response(
            self._send(req)
        )

    @keyword('Build Jenkins With Parameters')
    def build_jenkins_with_parameters(self, name=None, data=None):
        """Build Jenkins With Parameters

        Trigger build job jenkins

        Arguments:
            - name: fullname of job ``str``
            - data: job's parameters ``str``

        Return build number of starting job ``int``

        Examples:
        | ${build_number}= | Build Jenkins With Parameters | ${job_full_name} | ${parameters_string} |
        """
        if not name:
            raise Exception('Job name should not be None')
        job_detail = self.get_jenkins_job(name)
        req = self._session.prepare_request(
            requests.Request(
                'POST',
                self._job_url(BUILD_JOB_WITH_PARAMETERS, [self._job_folder(name)]),
                data=data
            )
        )
        response = self._send(req)
        response.raise_for_status()
        return job_detail['nextBuildNumber']

    @keyword('Build Jenkins And Get Build Status')
    def build_jenkins_and_get_build_status(self, name=None, data=None, response_bool=False,
                                           expect_result='SUCCESS', expect_building=False):
        """Build Jenkins And Get Build Status

        Trigger build job jenkins and wait until build job done

        Arguments:
            - name: fullname of job ``str``
            - data: job's parameters ``str``
            - response_bool: select response type [boolean] or [dictionary] ``bool``
            - expect_result: expect result from job information ``str``
            - expect_building: expect building from job information ``bool``

        Return dictionary of job information ``dict``

        Examples:
        | ${build_status}= | Build Jenkins And Get Build Status | ${job_full_name} | ${parameters_string} |
        """
        if not name:
            raise Exception('Job name should not be None')
        next_build_no = self.build_jenkins_with_parameters(name, data)
        next_build_no = str(next_build_no)
        response = str()
        retry = 24
        retry_interval = 5
        for i in range(retry):
            time.sleep(retry_interval)
            try:
                response = self.get_jenkins_job_build(name, next_build_no)
                if response['result'] == expect_result and response['building'] == bool(expect_building):
                    return True if response_bool else response
            except self._requests.HTTPError as err:
                if '404 Client Error' in str(err):
                    pass
        if response_bool:
            return False
        return response

    def _send(self, req):
        return self._session.send(req, **self._settings)

    @staticmethod
    def _get_response(response):
        response.raise_for_status()
        return json.loads(response.content, encoding='utf-8')

    def _job_url(self, url_format, params):
        url = url_format.format(*params)
        return self._endpoint + url

    @staticmethod
    def _job_folder(name):
        path_list = name.split('/')
        folder_name = ''
        job_name = path_list[-1]
        if len(path_list) > 1:
            folder_name = 'job/' + '/job/'.join(path_list[:-1]) + '/'
        return folder_name + 'job/' + job_name
