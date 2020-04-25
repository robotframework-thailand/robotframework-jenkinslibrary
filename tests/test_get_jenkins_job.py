import unittest
import requests_mock
import requests
from JenkinsLibrary.jenkins_face import JenkinsFace


class GetJenkinsJobTest(unittest.TestCase):

    def setUp(self) -> None:
        self.jenkins = JenkinsFace()

    @requests_mock.Mocker()
    def test_get_jenkins_job_success(self, mock):
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

        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        result = self.jenkins.get_jenkins_job('folder_name/test_job')

        self.assertEqual(result['url'], 'http://localhost:8080/job/folder_name/job/test_job/')

    @requests_mock.Mocker()
    def test_get_jenkins_job_when_has_sub_folder_success(self, mock):
        mock.get(
            'http://username:password@localhost:8080/job/folder_name/job/sub_folder_name/job/test_job/api/json',
            json={
                "_class": "",
                "actions": [],
                "description": None,
                "displayName": "",
                "displayNameOrNull": "",
                "name": "",
                "url": "http://localhost:8080/job/folder_name/job/sub_folder_name/job/test_job/",
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

    @requests_mock.Mocker()
    def test_get_jenkins_job_when_has_no_folder_success(self, mock):
        mock.get(
            'http://username:password@localhost:8080/job/test_job/api/json',
            json={
                "_class": "",
                "actions": [],
                "description": None,
                "displayName": "",
                "displayNameOrNull": "",
                "name": "",
                "url": "http://localhost:8080/job/test_job/",
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

        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        result = self.jenkins.get_jenkins_job('test_job')

        self.assertEqual(result['url'], 'http://localhost:8080/job/test_job/')

    def test_get_jenkins_job_fail_when_name_is_none(self):
        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False
        try:
            self.jenkins.get_jenkins_job()
        except:
            raised = True
        self.assertTrue(raised)

    def test_get_jenkins_job_fail_when_name_is_empty(self):
        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False
        try:
            self.jenkins.get_jenkins_job("")
        except:
            raised = True
        self.assertTrue(raised)

    @requests_mock.Mocker()
    def test_get_jenkins_job_fail_when_exception(self, mock):
        mock.get(
            'http://username:password@localhost:8080/job/folder_name/job/test_job/api/json',
            exc=requests.exceptions.HTTPError
        )

        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False

        try:
            self.jenkins.get_jenkins_job('folder_name/test_job')
        except requests.exceptions.HTTPError:
            raised = True

        self.assertTrue(raised)
