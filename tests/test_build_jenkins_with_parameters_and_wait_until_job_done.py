import unittest
import requests_mock
import requests
from JenkinsLibrary.jenkins_face import JenkinsFace


class BuildJenkinsWithParametersAndWaitUntilJobDoneTest(unittest.TestCase):

    def setUp(self) -> None:
        self.jenkins = JenkinsFace()

    @requests_mock.Mocker()
    def test_build_jenkins_with_parameters_and_wait_until_job_done_success(self, mock):
        mock.get(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/api/json',
            json={
                "_class": "",
                "actions": [],
                "description": None,
                "displayName": "",
                "displayNameOrNull": "",
                "name": "",
                "url": "http://localhost:8080/job/folder_name/job/test_job/",
                "buildable": True,
                "builds": [],
                "color": "blue",
                "firstBuild": {},
                "healthReport": [],
                "inQueue": False,
                "keepDependencies": False,
                "lastBuild": {},
                "lastCompletedBuild": {},
                "lastFailedBuild": {},
                "lastStableBuild": {},
                "lastSuccessfulBuild": {},
                "lastUnstableBuild": None,
                "lastUnsuccessfulBuild": {},
                "nextBuildNumber": 1,
                "property": [],
                "queueItem": None,
                "concurrentBuild": False,
                "building": True
            }
        )

        mock.post(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/buildWithParameters',
            status_code=200
        )

        mock.get(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/1/api/json',
            json={
                "_class": "",
                "actions": [],
                "description": None,
                "displayName": "",
                "displayNameOrNull": "",
                "name": "",
                "url": "http://localhost:8080/job/folder_name/job/test_job/1/api/json",
                "buildable": True,
                "builds": [],
                "color": "blue",
                "firstBuild": {},
                "healthReport": [],
                "inQueue": False,
                "keepDependencies": False,
                "lastBuild": {},
                "lastCompletedBuild": {},
                "lastFailedBuild": {},
                "lastStableBuild": {},
                "lastSuccessfulBuild": {},
                "lastUnstableBuild": None,
                "lastUnsuccessfulBuild": {},
                "nextBuildNumber": 2,
                "property": [],
                "queueItem": None,
                "concurrentBuild": False,
                "building": False
            }
        )

        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        result = self.jenkins.build_jenkins_with_parameters_and_wait_until_job_done('folder_name/test_job', 'data_test')
        self.assertFalse(result['building'])

    def test_build_jenkins_with_parameters_and_wait_until_job_done_fail_when_name_is_none(self):
        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False
        try:
            self.jenkins.build_jenkins_with_parameters_and_wait_until_job_done()
        except Exception as error:
            self.assertEqual(str(error), 'Job name should not be None')
            raised = True
        self.assertTrue(raised)

    def test_build_jenkins_with_parameters_and_wait_until_job_done_when_name_is_empty(self):
        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False
        try:
            self.jenkins.build_jenkins_with_parameters_and_wait_until_job_done("")
        except Exception as error:
            self.assertEqual(str(error), 'Job name should not be None')
            raised = True
        self.assertTrue(raised)

    @requests_mock.Mocker()
    def test_build_jenkins_with_parameters_and_wait_until_job_done_when_http_exception(self, mock):
        mock.get(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/api/json',
            json={
                "_class": "",
                "actions": [],
                "description": None,
                "displayName": "",
                "displayNameOrNull": "",
                "name": "",
                "url": "http://localhost:8080/job/folder_name/job/test_job/",
                "buildable": True,
                "builds": [],
                "color": "blue",
                "firstBuild": {},
                "healthReport": [],
                "inQueue": False,
                "keepDependencies": False,
                "lastBuild": {},
                "lastCompletedBuild": {},
                "lastFailedBuild": {},
                "lastStableBuild": {},
                "lastSuccessfulBuild": {},
                "lastUnstableBuild": None,
                "lastUnsuccessfulBuild": {},
                "nextBuildNumber": 6,
                "property": [],
                "queueItem": None,
                "concurrentBuild": False,
                "building": True
            }
        )

        mock.post(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/buildWithParameters',
            status_code=200
        )

        mock.get(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/6/api/json',
            exc=requests.exceptions.HTTPError
        )

        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False

        try:
            self.jenkins.build_jenkins_with_parameters_and_wait_until_job_done('folder_name/test_job',
                                                                               'data_test', retry=1)
        except Exception as error:
            self.assertEqual(str(error), 'HTTP error: ')
            raised = True

        self.assertTrue(raised)

    @requests_mock.Mocker()
    def test_build_jenkins_with_parameters_and_wait_until_job_done_when_exception(self, mock):
        mock.get(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/api/json',
            json={
                "_class": "",
                "actions": [],
                "description": None,
                "displayName": "",
                "displayNameOrNull": "",
                "name": "",
                "url": "http://localhost:8080/job/folder_name/job/test_job/",
                "buildable": True,
                "builds": [],
                "color": "blue",
                "firstBuild": {},
                "healthReport": [],
                "inQueue": False,
                "keepDependencies": False,
                "lastBuild": {},
                "lastCompletedBuild": {},
                "lastFailedBuild": {},
                "lastStableBuild": {},
                "lastSuccessfulBuild": {},
                "lastUnstableBuild": None,
                "lastUnsuccessfulBuild": {},
                "nextBuildNumber": 1,
                "property": [],
                "queueItem": None,
                "concurrentBuild": False,
                "building": True
            }
        )

        mock.post(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/buildWithParameters',
            status_code=200
        )

        mock.get(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/1/api/json',
            exc=requests.exceptions.ConnectionError
        )

        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False

        try:
            self.jenkins.build_jenkins_with_parameters_and_wait_until_job_done('folder_name/test_job', 'data_test')
        except Exception as error:
            self.assertEqual(str(error), 'Error: ')
            raised = True

        self.assertTrue(raised)
