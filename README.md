# robotframework-jenkinslibrary
[![codecov](https://codecov.io/gh/Panchorn/robotframework-jenkinslibrary/branch/master/graph/badge.svg)](https://codecov.io/gh/Panchorn/robotframework-jenkinslibrary)

Jenkins wrapper library for robotframework

# Usage
```bash
pip install -U robotframework-jsonlibrary
```
# Example Test Case

*** Settings ***       |                       |                  |                 |                  |              |
---------------------- |---------------------- |----------------- |---------------- |----------------- |------------- |
Library                | JenkinsLibrary        | ${host}          | ${username}     | ${password}      | ${verify}    |
*** Test Cases ***     |                       |                  |                 |                  |              |
create session jenkins | ${protocol}           |                  |                 |                  |              |
${job_details}=        | Get Jenkins Job       | ${job_full_name} |                 |                  |              |
${job_build_details}=  | Get Jenkins Job Build | ${job_full_name} | ${build_number} |                  |              |
${build_number}=       | Build Jenkins With Parameters | ${job_full_name} | ${parameters_string} |     |              |
