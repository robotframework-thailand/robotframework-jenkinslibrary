import unittest
import requests_mock
import requests
from JenkinsLibrary.jenkins_face import JenkinsFace


class BuildJenkinsWithParametersTest(unittest.TestCase):

    def setUp(self) -> None:
        self.jenkins = JenkinsFace()

    @requests_mock.Mocker()
    def test_build_jenkins_with_parameters_success(self, mock):
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
                "concurrentBuild": False
            }
        )

        mock.post(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/buildWithParameters',
            status_code=200
        )

        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        result = self.jenkins.build_jenkins_with_parameters('folder_name/test_job', 'data_test')

        self.assertEqual(result, 1)

    def test_build_jenkins_with_parameters_fail_when_name_is_none(self):
        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False
        try:
            self.jenkins.build_jenkins_with_parameters()
        except:
            raised = True
        self.assertTrue(raised)

    def test_build_jenkins_with_parameters_when_name_is_empty(self):
        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False
        try:
            self.jenkins.build_jenkins_with_parameters("")
        except:
            raised = True
        self.assertTrue(raised)

    @requests_mock.Mocker()
    def test_build_jenkins_with_parameters_when_exception(self, mock):
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
                "concurrentBuild": False
            }
        )

        mock.post(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/buildWithParameters',
            exc=requests.exceptions.HTTPError
        )

        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False

        try:
            self.jenkins.build_jenkins_with_parameters('folder_name/test_job', 'data_test')
        except requests.exceptions.HTTPError:
            raised = True

        self.assertTrue(raised)