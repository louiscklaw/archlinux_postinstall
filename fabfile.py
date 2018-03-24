#!/usr/bin/env python3


from fabric.api import *


@task
def install_pacaur():
     local('curl https://gist.githubusercontent.com/tadly/0e65d30f279a34c33e9b/raw/dc2f868d161cf420725d75e0fc0f284e3e0b9f09/pacaur_install.sh | sh -')
     
@task
def install_new():
    local('pacaur -Sy linux linux-headers')
    local('pacaur -Sy zsh')
