#!/usr/bin/env python3


from fabric.api import *


from fab_gnome import *

@task
def install_pacaur():
    local('curl https://gist.githubusercontent.com/tadly/0e65d30f279a34c33e9b/raw/dc2f868d161cf420725d75e0fc0f284e3e0b9f09/pacaur_install.sh | sh -')
    local('pacaur -Sy --needed --noconfirm --noedit patch')

@task
def disable_error_report():
    local('sudo systemctl disable apport.service')

@task
def install_new1():

    local('pacaur -Sy --needed --noconfirm --noedit zsh tmux oh-my-zsh-git imwheel htop nmap httpie sshrc')
    local('pacaur -Sy --needed --noconfirm --noedit visual-studio-code-bin meld nerd-fonts-complete monaco gitkraken')
    local('pacaur -Sy --needed --noconfirm --noedit gedit-code-assistance editorconfig-gedit')
    local('pacaur -Sy --needed --noconfirm --noedit linux linux-headers')
    local('pacaur -Sy --needed --noconfirm --noedit virtualbox virtualbox-host-dkms virtualbox-ext-oracle vdfuse')
    local('pacaur -Sy --needed --noconfirm --noedit rclone filezilla')
    local('pacaur -Sy --needed --noconfirm --noedit rhythmbox remmina')
    local('pacaur -Sy --needed --noconfirm --noedit networkmanager-openconnect networkmanager-openvpn networkmanager-pptp')
    local('pacaur -Sy --needed --noconfirm --noedit google-cloud-sdk google-chrome')
    local('pacaur -Sy --needed --noconfirm --noedit android-studio genymotion scrcpy')
    local('pacaur -Sy --needed --noconfirm --noedit intellij-idea-ce  pycharm-community')
    local('pacaur -Sy --needed --noconfirm --noedit spotify discord signal')
    local('pacaur -Sy --needed --noconfirm --noedit ibus-cangjie')
    local('pacaur -Sy --needed --noconfirm --noedit guake')
    local('pacaur -Sy --needed --noconfirm --noedit ttf-emojione-color ttf-twemoji-color')
    local('pacaur -Sy --needed --noconfirm --noedit peek')
    local('pacaur -Sy --needed --noconfirm --noedit bitwarden')
    local('pacaur -Sy --needed --noconfirm --noedit vlc')
    local('pacaur -Sy --needed --noconfirm --noedit p7zip p7zip-plugins unrar tar rsync')

@task
def install_gnome_ext():
    list_ext=[
        'gnome-shell-extension-no-topleft-hot-corner',
        'gnome-shell-extension-gsconnect',
        'gnome-shell-pomodoro',
        'gtk-theme-arc-git',
        'gnome-shell-extension-mediaplayer-git',
        'gnome-shell-extension-topicons-plus',
        'gnome-shell-extension-no-title-bar-git',
        'gnome-shell-extension-caffeine-git',
        'gnome-shell-extension-extended-gestures-git'
    ]
    for ext in list_ext:
        local('pacaur -Sy --needed --noconfirm --noedit  {}'.format(ext))

@task
def install_pip():
    local('sudo pip install --upgrade pip')
    list_pip=['pipenv']
    results=[local('sudo pip install {}'.format(pip_pkg))  for pip_pkg in list_pip]
