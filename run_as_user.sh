#!/bin/sh

OLD_UID=$1
OLD_GID=$2
shift; shift

useradd --uid $OLD_UID --gid $OLD_GID --non-unique user

HOME=$HOME \
    sudo -E -u user "$@"
