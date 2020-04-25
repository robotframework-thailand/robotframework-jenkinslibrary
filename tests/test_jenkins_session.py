import unittest
from JenkinsLibrary.jenkins_face import JenkinsFace


class JenkinsSessionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.jenkins = JenkinsFace()

    def test_create_session_success(self):
        self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', 'password', False)
        session = self.jenkins._session
        settings = self.jenkins._settings
        endpoint = self.jenkins._endpoint
        self.assertIsNotNone(session)
        self.assertFalse(settings['verify'])
        self.assertFalse(settings['allow_redirects'])
        self.assertEqual('http://username:password@localhost:8080/', endpoint)

    def test_create_session_fail_when_url_is_none(self):
        raised = False
        try:
            self.jenkins.create_session_jenkins('http', None, 'username', 'password', False)
        except:
            raised = True
        self.assertTrue(raised)

    def test_create_session_fail_when_username_is_none(self):
        raised = False
        try:
            self.jenkins.create_session_jenkins('http', 'localhost:8080', None, 'password', False)
        except:
            raised = True
        self.assertTrue(raised)

    def test_create_session_fail_when_password_is_none(self):
        raised = False
        try:
            self.jenkins.create_session_jenkins('http', 'localhost:8080', 'username', None, False)
        except:
            raised = True
        self.assertTrue(raised)
