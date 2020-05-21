from .jenkins_face import JenkinsFace
from .version import VERSION

__version__ = VERSION


class JenkinsLibrary(JenkinsFace):
    """JenkinsLibrary is a robotframework library for wrapping jenkins api

    == Example Test Cases ==
    | *** Settings ***       |
    | Library                | JenkinsLibrary   |
    |                        |
    | *** Test Cases ***     |
    | create session jenkins | ${protocol}      | ${host}          | ${username}      | ${password}      | ${verify} |
    | ${job_details}=        | Get Jenkins Job  | ${job_full_name} |
    | ${job_build_details}=  | Get Jenkins Job Build | ${job_full_name} | ${build_number}  |
    | ${build_number}=       | Build Jenkins With Parameters | ${job_full_name} | ${parameters_string} |
    | ${job_build_details}=  | Build Jenkins With Parameters And Wait Until Job Done | ${job_full_name} | ${parameters_string} | 10 | 2 |

    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
