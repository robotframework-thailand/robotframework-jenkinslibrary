import unittest
from JenkinsLibrary.jenkins_face import JenkinsFace


class JenkinsSessionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.jenkins = JenkinsFace()

    def test_delete_snapshot_with_delete_key(self):
        self.jenkins.create_session_jenkins('a', 'a', 'a', 'a')
        self.assertIsNotNone(self.jenkins._session)

    if __name__ == '__main__':
        unittest.main()
