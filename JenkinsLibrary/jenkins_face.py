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

    @keyword('Build Jenkins With Parameters And Wait Until Job Done')
    def build_jenkins_with_parameters_and_wait_until_job_done(self, name=None, data=None, retry=24, retry_interval=5):
        """Build Jenkins With Parameters And Wait Until Job Done

        Trigger build job jenkins and wait until build job done

        Arguments:
            - name: fullname of job ``str``
            - data: job's parameters ``str``
            - retry: number of times to retry ``int`` ``default is 24``
            - retry_interval: time to wait before checking job status again ``int`` ``default is 5``

        Return dictionary of job information if job done ``dict``, otherwise will return ``None``

        Examples:
        | ${job_build_details}= | Build Jenkins With Parameters And Wait Until Job Done | ${job_full_name} | ${parameters_string} | 10 | 2 |
        """
        if not name:
            raise Exception('Job name should not be None')
        next_build_no = self.build_jenkins_with_parameters(name, data)
        for _ in range(retry):
            time.sleep(retry_interval)
            try:
                response = self.get_jenkins_job_build(name, next_build_no)
                if response['building'] == False:
                    return response
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 404:
                    pass
                else:
                    raise err
            except Exception as err:
                raise err

    def _send(self, req):
        return self._session.send(req, **self._settings)

    @staticmethod
    def _get_response(response):
        response.raise_for_status()
        return json.loads(response.content)

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
