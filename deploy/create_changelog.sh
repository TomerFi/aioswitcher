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
	echo "Script creating a CHANGELOG.md file for the next release"
	echo "--------------------------------------------------------"
	echo "Usage: $0 -h/--help"
	echo "Usage: $0 --tag <tag>"
	echo "Usage: $0 --tag <tag> --preset <preset>"
	echo ""
	echo "Example: $0 --tag 2.1.17"
	echo "Example: $0 --tag 2.1.17 --preset conventionalcommits"
	echo ""
	echo "** requires nodejs >= 14.0.0"
	echo "** requires 'npm i -g conventional-changelog-cli'"
}
# show usage if asked for help
if [[ ($1 == "--help") || $1 == "-h" ]]; then
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
preset=${preset:-conventionalcommits}
# if no --tag provided show usage and exit
if [ -z "$tag" ]; then
	show_usage
	exit 1
fi
# remove previous CHANGELOG.md file
rm -f CHANGELOG.md
# create a temporary release context file
echo "{\"version\": \"$tag\"}" >release-context.json
# use conventional-change-log to generate the CHANGELOG.md file
conventional-changelog -p $preset -t "" -c release-context.json -o CHANGELOG.md
# delete the temporary release context file
rm -f release-context.json
