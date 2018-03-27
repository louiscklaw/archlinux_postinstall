#!/usr/bin/env python3

import os
import sys

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.project import *

# git config --global user.email "logickee@gmail.com"
# git config --global user.name "logickee"
# git config --global core.editor "vim"
# sudo apt install -qqy  git  fabric

CWD = os.path.dirname(os.path.abspath(__file__))
PROJ_HOME = [
    CWD,
    '/home/logic/_tmp'
]


@task
def bootstrap_git():
    rsync_project(
        remote_dir=PROJ_HOME[1],
        local_dir=PROJ_HOME[0]+'/'
    )
    run('sudo apt install -qqy  git  fabric')
    run('git config --global user.email "logickee@gmail.com"')
    run('git config --global user.name "logickee"')
    run('git config --global core.editor "vim"')
    run('cat /dev/zero | ssh-keygen -q -N ""')

    run('mkdir -p {}'.format(PROJ_HOME[1]))


def get_lsbrelease():
    return local('lsb_release -c -s',capture=True)

def apt_install_package(list_package):
    local('sudo apt install -qqy {}'.format(list_package))


@task
def install_gterminal_theme():
    # https://github.com/Mayccoll/Gogh/blob/master/content/themes.md
    local('sudo apt-get install -qqy dconf-cli')
    local('wget -O xt  http://git.io/v3D8e && chmod +x xt && ./xt && rm xt')

@task
def install_pycharm():
    local('sudo add-apt-repository -y -u ppa:ubuntu-desktop/ubuntu-make')
    local('sudo apt-get update')
    local('sudo apt-get install -qqy ubuntu-make')
    local('umake ide pycharm idea')

@task
def install_zsh():
    apt_install_package('zsh wget')
    local('wget --no-check-certificate https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh')
    local('sudo chsh -s /usr/bin/zsh')


@task
def install_sshrc():
    local('wget --no-check-certificate https://raw.githubusercontent.com/Russell91/sshrc/master/sshrc')
    local('chmod +x sshrc')
    local('sudo mv sshrc /usr/local/bin')

@task
def install_spotify():
    # 1. Add the Spotify repository signing keys to be able to verify downloaded packages
    # 2. Add the Spotify repository
    # 3. Update list of available packages
    # 4. Install Spotify
    local('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0DF731E45CE24F27EEEB1450EFDC8610341D9410')
    local('echo deb http://repository.spotify.com stable non-free | sudo tee /etc/apt/sources.list.d/spotify.list')
    local('sudo apt-get update')
    local('sudo apt-get install -qqy spotify-client')

@task
def install_new():
    # local('sudo apt install -qqy meld nerd-fonts-complete monaco gitkraken')
    # local('sudo apt install -qqy gedit-code-assistance editorconfig-gedit')
    # vdfuse
    # local('sudo apt install -qqy android-studio genymotion scrcpy')
    # local('sudo apt install -qqy discord signal')
    # local('sudo apt install -qqy ibus-cangjie')
    # local('sudo apt install -qqy ttf-emojione-color ttf-twemoji-color')
    # local('sudo apt install -qqy peek')
    # local('sudo apt install -qqy bitwarden')

    packages_list=[
        # 'gnome-shell-extension-tilix-dropdown', 'tilix',
        'vlc',
        'p7zip unrar tar rsync',
        'network-manager-openconnect network-manager-openvpn network-manager-pptp',
        'rhythmbox remmina',
        # 'rclone',
        'filezilla',
        'virtualbox virtualbox-dkms virtualbox-ext-pack',
        'tmux  imwheel htop nmap httpie ',
        'net-tools',
        'python3-pip'
    ]

    for package in packages_list:
        apt_install_package(package)

@task
def install_docker():
    output_from_lsbrelese = get_lsbrelease()
    local('sudo apt-get remove docker docker-engine docker.io')
    local('sudo apt-get install -qqy apt-transport-https ca-certificates curl software-properties-common')
    local('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -')
    local('sudo add-apt-repository  "deb [arch=amd64] https://download.docker.com/linux/ubuntu  {}  stable"'.format(output_from_lsbrelese))
    local('sudo apt-get update')
    local('sudo apt-get install -qqy docker-ce')
    local('docker --version')

    # install docker-compose
    local('sudo curl -L https://github.com/docker/compose/releases/download/1.20.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose')
    local('sudo chmod +x /usr/local/bin/docker-compose')
    local('docker-compose --version')


    local('sudo systemctl enable docker')

@task
def install_vim():
    local('sudo apt install -qqy vim')
    local('curl https://j.mp/spf13-vim3 -L > spf13-vim.sh && sh spf13-vim.sh')

@task
def install_google_cloud_sdk():
    ubuntu_code_version=get_lsbrelease()
    CLOUD_SDK_REPO_ENV_VAR = 'cloud-sdk-{}'.format(ubuntu_code_version)

    # Add the Cloud SDK distribution URI as a package source
    local('echo "deb http://packages.cloud.google.com/apt {} main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list'.format(CLOUD_SDK_REPO_ENV_VAR))

    # Import the Google Cloud Platform public key
    local('curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -')

    # Update the package list and install the Cloud SDK
    local('sudo apt-get update && sudo apt-get install -qqy google-cloud-sdk')

@task
def install_theme():
    # local('sudo add-apt-repository ppa:noobslab/icons')

    local('sudo add-apt-repository -y -u  ppa:snwh/pulp')
    local('sudo add-apt-repository -y -u  ppa:noobslab/themes')
    local('sudo apt-get update')

    local('sudo apt-get install -qqy arc-theme paper-icon-theme')

@task
def install_gnome_ext():
    list_ext=[
        'gnome-shell-extensions',
        # 'gnome-shell-extension-dashtodock',
        'gnome-shell-pomodoro',
        # 'gnome-shell-extension-mediaplayer',
        'gnome-shell-extension-caffeine'
        # 'gnome-shell-extension-no-topleft-hot-corner',
        # 'gnome-shell-extension-gsconnect',
        # 'gnome-shell-extension-topicons-plus',
        # 'gnome-shell-extension-no-title-bar',
        # 'gnome-shell-extension-extended-gestures'
    ]
    for ext in list_ext:
        apt_install_package(ext)

    # local('sudo apt-get remove gnome-shell-extension-ubuntu-dock')
    local('gsettings set org.gnome.shell enable-hot-corners false')

@task
def install_cursor():
    local('git clone https://github.com/keeferrourke/capitaine-cursors.git')
    local('mkdir -p ~/.icons/capitaine-cursors')
    local('cp -pr capitaine-cursors/dist/ ~/.icons/capitaine-cursors')

@task
def bootstrap_vscode_settings():
    setting_file='/home/logic/.config/Code/User/settings.json'
    run('mkdir -p {}'.format(os.path.dirname(setting_file)))
    rsync_project(
        local_dir='/home/logic/.config/Code/User/settings.json',
        remote_dir='/home/logic/.config/Code/User/settings.json'
    )

@task
def install_vscode():
    local('sudo apt install -qqy curl')
    local('curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg')
    local('sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg')
    local('''sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list' ''')
    local('sudo apt update')
    local('sudo apt install -qqy code')


@task
def install_nvidia():
    local('sudo apt  install -qqy nvidia-384')

@task
def install_pip():
    local('sudo apt install -qqy python3-pip')
    local('sudo pip3 install --upgrade pip')
    list_pip=['pipenv']
    results=[local('sudo pip3 install {}'.format(pip_pkg))  for pip_pkg in list_pip]

@task
def gnome_natural_scrolling():
    local('gsettings set org.gnome.desktop.peripherals.mouse natural-scroll true')
    local('gsettings set org.gnome.desktop.peripherals.touchpad natural-scroll true')


@task
def fallback_origional_gnome():
    local('sudo apt install -qqy gnome-session ubuntu-gnome-default-settings')
    local('sudo apt install -qqy vanilla-gnome-default-settings vanilla-gnome-desktop')


    # local('sudo update-alternatives --config gdm3.css')
    # local('sudo apt install -qqy gnome-maps gnome-weather polari gnome-documents gnome-photos gnome-music')
