import unittest
import requests_mock
import requests
from JenkinsLibrary.jenkins_face import JenkinsFace


class GetJenkinsJobTest(unittest.TestCase):

    def setUp(self) -> None:
        self.jenkins = JenkinsFace()

    @requests_mock.Mocker()
    def test_get_jenkins_job_build_success_with_last_build(self, mock):
        mock.get(
            'http://username:password@localhost:8080/job/test/lastBuild/api/json',
            json={
                "_class": "",
                "actions": [],
                "description": None,
                "displayName": "",
                "displayNameOrNull": "",
                "name": "",
                "url": "http://localhost:8080/job/test/",
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
        result = self.jenkins.get_jenkins_job_build('job/test')

        self.assertEqual(result['url'], 'http://localhost:8080/job/test/')

    @requests_mock.Mocker()
    def test_get_jenkins_job_build_success(self, mock):
        mock.get(
            'http://username:password@localhost:8080/job/test/99/api/json',
            json={
                "_class": "",
                "actions": [],
                "description": None,
                "displayName": "",
                "displayNameOrNull": "",
                "name": "",
                "url": "http://localhost:8080/job/test/",
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
        result = self.jenkins.get_jenkins_job_build('job/test', '99')

        self.assertEqual(result['url'], 'http://localhost:8080/job/test/')

    def test_get_jenkins_job_build_fail_when_name_is_none(self):
        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False
        try:
            self.jenkins.get_jenkins_job_build()
        except:
            raised = True
        self.assertTrue(raised)

    def test_get_jenkins_job_build_fail_when_name_is_empty(self):
        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False
        try:
            self.jenkins.get_jenkins_job_build("")
        except:
            raised = True
        self.assertTrue(raised)

    @requests_mock.Mocker()
    def test_get_jenkins_job_build_fail_when_exception(self, mock):
        mock.get(
            'http://username:password@localhost:8080/job/test/lastBuild/api/json',
            exc=requests.exceptions.HTTPError
        )

        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        raised = False

        try:
            self.jenkins.get_jenkins_job_build('job/test')
        except requests.exceptions.HTTPError:
            raised = True

        self.assertTrue(raised)
