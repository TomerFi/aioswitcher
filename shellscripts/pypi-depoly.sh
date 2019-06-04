#!/bin/bash

# pypi-depoly.sh
#
# Script for optionally deploying packages to pypi.
# Takes the git tag value as the first argument,
# Takes the pypi username as second argument,
# Takes the pypi password as third argument,
# takes the full path of the setuf.cfg file as the fourth argument.
# If the git tag euqals to the version set in the setup.cfg file,
# the script will upload the the package to pypi using the supllied credentials.

display_usage() {
    echo "please provide git tag, pypi username, pypi password and the path of the setup.cfg file as arguments."
    echo -e "the git tag will be evaluated against the version in the setup.cfg file.\n"
    echo "usage: $0 gittag pypiuser pypipassword /mypath/setup.cfg"
}


if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]
then
    display_usage
    exit 1
fi

version=$(awk -F"=" '/^version/ { print $2 }' "$4")

if [ "$1" == "$version" ]
then
  echo "Creating the .pypirc file."
  
  {
    echo -e "[pypi]"
    echo -e "username = $2"
    echo -e "password = $3"
  } >> ~/.pypirc

  echo "Deploying version $1 to pypi using twine."
  rm -rf dist/*
  setup.py sdist bdist_wheel
  twine upload dist/*

else
  echo "Not deployable, pypi version $1 and git tag $version are not euqal."

fi

exit 0
