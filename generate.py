#!/usr/bin/env python
from os.path import join, dirname
from robot.libdoc import libdoc


def main():
    libdoc(join(dirname(__file__), 'JenkinsLibrary'), join(dirname(__file__), 'docs', 'JenkinsLibrary.html'))


if __name__ == '__main__':
    main()
