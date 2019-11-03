#!/bin/bash

LOCAL_CONFIG=test-config.local
REQ_EXECUTABLES="STEF MYSH"

# See this one on what variables to set.
source ./test-config

# You can overwrite variables set in ./test-config here so that you don't need
# to fix them every time you sync with the STEF repo.
[[ -f $LOCAL_CONFIG ]] && source $LOCAL_CONFIG

for v in $REQ_EXECUTABLES; do
	value=$( eval echo \$$v )

	if [[ -z "$value" ]]; then
	    echo "Variable $v must be defined.  Exiting."
	    exit 1
	fi

	if [[ ! -f $value || ! -x $value ]]; then
	    echo "$value not found or not executable.  Exiting."
	    exit 1
	fi
done

$STEF $*
