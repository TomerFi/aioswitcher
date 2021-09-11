#!/bin/bash

# Copyright Tomer Figenblat.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
#limitations under the License.

show_usage() {
	echo "Script returing the next java development iteration for a semantic version"
	echo "--------------------------------------------------------------------------"
	echo "Usage: $0 -h/--help"
	echo "Usage: $0 --tag <tag>"
	echo ""
	echo "Example: $0 --tag 2.1.17"
	echo "Example: $0 --tag 2.1.17 --label .dev"
	echo "Will output: 2.1.18.dev"
}
if [[ ($# == "--help") || $# == "-h" ]]; then
	show_usage
	exit 0
fi
# iterate over arguments and create named parameters
while [ $# -gt 0 ]; do
	if [[ $1 == *"--"* ]]; then
		param="${1/--/}"
		declare $param="$2"
	fi
	shift
done
# default named parameters
label=${label:-.dev}
# if no --tag provided show usage and exit
if [ -z "$tag" ]; then
	show_usage
	exit 1
fi
# utility function for incrementing the bump number
increment() { echo $(("$1" + 1)); }
# extract the major_minor and patch parts from the version
new_major_minor=$(cut -f1,2 -d"." <<<$tag)
new_patch=$(cut -d"." -f3- <<<$tag)
# increment the patch part
next_patch=$(increment $new_patch)
# concatenate the new major, minor, and next patch parts with the .dev suffix
next_iteration=$new_major_minor.$next_patch$label
# return the next development iteration
echo $next_iteration
