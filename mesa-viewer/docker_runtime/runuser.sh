#!/bin/bash

# Run CMD using exec as RUN_USER to avoid security issues, static-file chown issues

echo "== runuser.sh =="
echo Uid: $RUN_UID
echo Gid: $RUN_GID
echo Cmd: "\"$CMD\""

# CMD as specified in Dockerfile
CMD="$@"

# Check if a run user was specified
if [ "$RUN_UID" -ne "0" ]; then
    # Set groupid equal to userid if not specified
    if [ -z "$RUN_GID" ]; then
        RUN_GID=$RUN_UID
    fi
    # Create a user with uid and gid specified and run a bash session as that user with parameters as passed
    addgroup --gid=$RUN_GID runuser
    adduser --gecos "" --disabled-password --uid=$RUN_UID --gid=$RUN_GID runuser
    RUN_USER=runuser
else
    # Default to root user
    RUN_USER=root
fi

echo "================"

set -x

# Run CMD using exec as RUN_USER to avoid security issues, static-file chown issues
# and sub-process signal issues, see http://www.projectatomic.io/docs/docker-image-author-guidance/
su $RUN_USER -c "exec $CMD"
