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

# usecase
# install_gnome_accessories install_vscode
# fab fallback_origional_gnome install_cursor install_theme install_cursor install_nvidia
# fab install_vim install_zsh   bootstrap_vscode_settings
# fab install_sw  install_pip   install_pycharm install_gterminal_theme install_docker
# fab install_spotify install_sshrc install_google_cloud_sdk


CWD = os.path.dirname(os.path.abspath(__file__))
PROJ_HOME = [
    CWD,
    '/home/logic/_tmp'
]

@task
def download_fonts():
    local('wget https://raw.githubusercontent.com/todylu/monaco.ttf/master/monaco.ttf')
    local('wget https://gist.github.com/epegzz/1634235/raw/4691e901750591f9cab0b4ae8b7c0731ebf28cce/Monaco_Linux-Powerline.ttf')
    sudo('sudo add-apt-repository -y -u ppa:eosrei/fonts')
    sudo('sudo apt update && sudo apt install fonts-emojione-svginot')


@task
def bootstrap_git():
    # rsync_project(
    #     remote_dir=PROJ_HOME[1],
    #     local_dir=PROJ_HOME[0]+'/'
    # )
    sudo('apt install php7 python3 python3-pip python2 python2-pip')
    sudo('apt install -qqy  git  fabric')
    run('git config --global user.email "logickee@gmail.com"')
    run('git config --global user.name "logickee"')
    run('git config --global core.editor "vim"')
    # run('cat /dev/zero | ssh-keygen -q -N ""')

    # run('mkdir -p {}'.format(PROJ_HOME[1]))


@task
def get_lsbrelease():
    release_name = run('lsb_release -c -s')
    release_name = release_name.strip()
    print(release_name)
    return release_name


def apt_install_package(list_package):
    with settings(warn_only=True):
        sudo('apt install -qqy {}'.format(list_package))


@task
def install_ng_wallpaper():
    sudo('add-apt-repository -y -u ppa:atareao/atareao')
    sudo('apt-get update')
    sudo('apt-get install national-geographic-wallpaper')


@task
def install_gterminal_theme():
    # https://github.com/Mayccoll/Gogh/blob/master/content/themes.md
    sudo('apt-get install -qqy dconf-cli')
    run('wget -O xt  http://git.io/v3D8e && chmod +x xt && ./xt && rm xt')


@task
def install_pycharm():
    sudo('snap install pycharm-community --classic')
    sudo('snap install intellij-idea-community --classic')


@task
def install_zsh():
    #
    apt_install_package('zsh wget git tig git-flow fonts-powerline')
    run('wget --no-check-certificate https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh')
    sudo('chsh -s /usr/bin/zsh')

    put('/home/logic/.zshrc', '/home/logic')


@task
def sync_gnome_extensions():
    rsync_project(
        local_dir='/home/logic/.local/share/gnome-shell/extensions/',
        remote_dir='/home/logic/.local/share/gnome-shell/extensions'
    )
    list_extensions = [
        'dash-to-dock@micxgx.gmail.com',
        'dynamicTopBar@gnomeshell.feildel.fr',
        'mconnect@andyholmes.github.io',
        'nohotcorner@azuri.free.fr',
        'no-title-bar@franglais125.gmail.com',
        'ShellTile@emasab.it',
    ]

    with settings(warn_only=True):
        [run('gnome-shell-extension-tool -e ' + extension) for extension in list_extensions]


@task
def install_ng_wallpaper():
    # install national grographic wallpaper
    sudo('add-apt-repository -y -u ppa:atareao/atareao')
    sudo('apt-get update')
    sudo('apt-get install -qqy national-geographic-wallpaper')


@task
def install_tmux():
    # https://github.com/gpakosz/.tmux
    sudo('apt install -qqy tmux')
    with cd('/home/logic'):
        run('rm -rf .tmux')
        run('git clone https://github.com/gpakosz/.tmux.git')
        run('ln -s -f .tmux/.tmux.conf')
        run('cp .tmux/.tmux.conf.local .')


@task
def install_sshrc():
    run('wget --no-check-certificate https://raw.githubusercontent.com/Russell91/sshrc/master/sshrc')
    run('chmod +x sshrc')
    sudo('mv sshrc /usr/local/bin')


@task
def install_spotify():
    # 1. Add the Spotify repository signing keys to be able to verify downloaded packages
    # 2. Add the Spotify repository
    # 3. Update list of available packages
    # 4. Install Spotify
    sudo('apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0DF731E45CE24F27EEEB1450EFDC8610341D9410')
    run('echo deb http://repository.spotify.com stable non-free | sudo tee /etc/apt/sources.list.d/spotify.list')
    sudo('apt-get update')
    sudo('apt-get install -qqy spotify-client')


@task
def install_sw():
    # sudo('apt install -qqy meld nerd-fonts-complete monaco gitkraken')
    # sudo('apt install -qqy gedit-code-assistance editorconfig-gedit')
    # vdfuse
    # sudo('apt install -qqy android-studio genymotion scrcpy')
    # sudo('apt install -qqy discord signal')
    # sudo('apt install -qqy ibus-cangjie')
    # sudo('apt install -qqy ttf-emojione-color ttf-twemoji-color')
    # sudo('apt install -qqy peek')
    # sudo('apt install -qqy bitwarden')

    packages_list = [
        # 'gnome-shell-extension-tilix-dropdown', 'tilix',
        'wget', 'curl',
        'vlc',
        'p7zip unrar tar rsync',
        'network-manager-openconnect network-manager-openvpn network-manager-pptp',
        'rhythmbox remmina',
        # 'rclone',
        'filezilla',
        'virtualbox virtualbox-dkms virtualbox-ext-pack',
        'imwheel htop nmap httpie ',
        'net-tools',
        'python3-pip',
        'glances', 'htop', 'iotop',
        'ibus-cangjie', 'guake',
        'chromium-bsu', 'uget',
        'meld'
    ]

    for package in packages_list:
        apt_install_package(package)


@task
def install_docker():
    output_from_lsbrelese = get_lsbrelease()
    sudo('apt-get remove docker docker-engine docker.io')
    sudo('apt-get install -qqy apt-transport-https ca-certificates curl software-properties-common')
    sudo('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -')
    sudo('add-apt-repository -y -u "deb [arch=amd64] https://download.docker.com/linux/ubuntu  {}  stable"'.format(output_from_lsbrelese))
    sudo('apt-get update')
    sudo('apt-get install -qqy docker-ce')
    run('docker --version')

    # install docker-compose
    sudo('curl -L https://github.com/docker/compose/releases/download/1.20.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose')
    sudo('chmod +x /usr/local/bin/docker-compose')
    run('docker-compose --version')

    sudo('systemctl enable docker')


@task
def install_vim():
    sudo('apt install -qqy vim curl')
    run('curl https://j.mp/spf13-vim3 -L > spf13-vim.sh && sh spf13-vim.sh')


@task
def install_google_cloud_sdk():
    ubuntu_code_version = get_lsbrelease()
    CLOUD_SDK_REPO_ENV_VAR = 'cloud-sdk-{}'.format(ubuntu_code_version)

    # Add the Cloud SDK distribution URI as a package source
    run('echo "deb http://packages.cloud.google.com/apt {} main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list'.format(CLOUD_SDK_REPO_ENV_VAR))

    # Import the Google Cloud Platform public key
    run('curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -')

    # Update the package list and install the Cloud SDK
    sudo('apt-get update && sudo apt-get install -qqy google-cloud-sdk')


@task
def install_theme():
    # sudo('add-apt-repository ppa:noobslab/icons')

    sudo('add-apt-repository -y -u  ppa:snwh/pulp')
    sudo('add-apt-repository -y -u  ppa:noobslab/themes')
    sudo('apt-get update')

    sudo('apt-get install -qqy arc-theme paper-icon-theme')


@task
def install_gnome_accessories():
    list_ext = [
        # 'gnome-shell-extensions',
        # 'gnome-shell-extension-dashtodock',
        'gnome-shell-pomodoro',
        'gnome-shell-extension-mediaplayer',
        'gnome-shell-extension-caffeine',
        'gnome-shell-extension-tilix-dropdown',
        'gnome-shell-extensions-gpaste',
    ]

    list_ext += ['ibus-cangjie']
    for ext in list_ext:
        apt_install_package(ext)

    sudo('apt remove -y gnome-shell-extension-ubuntu-dock ubuntu-desktop')

    # sudo('apt-get remove gnome-shell-extension-ubuntu-dock')


@task
def install_cursor():
    run('rm -rf capitaine-cursors')
    run('git clone https://github.com/keeferrourke/capitaine-cursors.git')
    run('mkdir -p ~/.icons/capitaine-cursors')
    run('cp -pr capitaine-cursors/dist/ ~/.icons/capitaine-cursors')


@task
def bootstrap_vscode_settings():
    setting_file = '/home/logic/.config/Code/User/settings.json'
    run('mkdir -p {}'.format(os.path.dirname(setting_file)))
    rsync_project(
        local_dir='/home/logic/.config/Code/User/settings.json',
        remote_dir='/home/logic/.config/Code/User/settings.json'
    )


@task
def install_vscode():
    sudo('apt install -qqy curl')
    run('curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg')
    sudo('mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg')
    sudo('''sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list' ''')
    sudo('apt update')
    sudo('apt install -qqy code zeal')


@task
def install_nvidia():
    sudo('apt  install -qqy nvidia-384')


@task
def install_pip():
    sudo('apt install -qqy python3-pip')
    sudo('pip3 install --upgrade pip')
    list_pip = ['pipenv', 'pylint', 'pydocstyle', 'autopep8']
    results = [sudo('pip3 install {}'.format(pip_pkg)) for pip_pkg in list_pip]


@task
def gnome_natural_scrolling():
    run('gsettings set org.gnome.desktop.peripherals.mouse natural-scroll true')
    run('gsettings set org.gnome.desktop.peripherals.touchpad natural-scroll true')
    run('gsettings set org.gnome.shell enable-hot-corners false')


@task
def fallback_origional_gnome():
    sudo('apt install -qqy gnome-session ubuntu-gnome-default-settings')
    sudo('apt install -qqy vanilla-gnome-default-settings vanilla-gnome-desktop')

    # sudo('update-alternatives --config gdm3.css')
    # sudo('apt install -qqy gnome-maps gnome-weather polari gnome-documents gnome-photos gnome-music')

@task
def install_cura():
    sudo('add-apt-repository -u -y ppa:thopiekar/cura')
    sudo('apt-get update ')
    sudo('apt-get install -qqy cura')
