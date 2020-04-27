from .jenkins_face import JenkinsFace
from .version import VERSION

__version__ = VERSION


class JenkinsLibrary(JenkinsFace):
    """JenkinsLibrary is a robotframework library for wrapping jenkins api

    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
