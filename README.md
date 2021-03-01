# robotframework-jenkinslibrary
[![codecov](https://codecov.io/gh/robotframework-thailand/robotframework-jenkinslibrary/branch/master/graph/badge.svg)](https://codecov.io/gh/robotframework-thailand/robotframework-jenkinslibrary)
[![PyPI](https://img.shields.io/pypi/v/robotframework-jenkinslibrary.svg)](https://pypi.org/project/robotframework-jenkinslibrary/)

Jenkins wrapper library for robotframework

## Usage
Install package by using pip:
```bash
pip install -U robotframework-jenkinslibrary
```
## Example Test Case

*** Settings ***       |                       |                  |                 |                  |                  |
---------------------- |---------------------- |----------------- |---------------- |----------------- |----------------- |
Library                | JenkinsLibrary        |                  |                 |                  |                  |
*** Test Cases ***     |                       |                  |                 |                  |                  |
create session jenkins | ${protocol}           | ${host}          | ${username}     | ${password}      | ${verify}        |
${job_details}=        | Get Jenkins Job       | ${job_full_name} |                 |                  |                  |
${job_build_details}=  | Get Jenkins Job Build | ${job_full_name} | ${build_number} |                  |                  |
${build_number}=       | Build Jenkins With Parameters | ${job_full_name} | ${parameters_string} |     |                  |
${job_build_details}=  | Build Jenkins With Parameters And Wait Until Job Done | ${job_full_name} | ${parameters_string} | 10 | 2 |

## Document
For more keyword detail go to the following link:
https://robotframework-thailand.github.io/robotframework-jenkinslibrary/

## Uninstall package
```bash
pip uninstall robotframework-jenkinslibrary 
```

## Feature Status
| API | Status |
|---|---|
| Get Jenkins Job | + |
| Get Jenkins Job Build | + |
| Build Jenkins With Parameters | + |
| Build Jenkins With Parameters And Wait Until Job Done | + |
| - | - |