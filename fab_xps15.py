#!/usr/bin/env python3


from fabric.api import *

#   git config --global user.email "logickee@gmail.com"
#   git config --global user.name "logickee"

# sudo apt install -qqy  git python3-pip 



def apt_install_package(list_package):
    local('sudo apt install -qqy {}'.format(' '.join(list_package)))

@task
def install_zsh():
    apt_install_package(['zsh','wget'])
    local('wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh')
    sudo('chsh -s `which zsh`')
    
@task
def install_new():
    # local('sudo apt install -qqy meld nerd-fonts-complete monaco gitkraken')
    # local('sudo apt install -qqy gedit-code-assistance editorconfig-gedit')
    # local('sudo apt install -qqy linux linux-headers')
    # vdfuse
    # local('sudo apt install -qqy google-cloud-sdk google-chrome')
    # local('sudo apt install -qqy android-studio genymotion scrcpy')
    # local('sudo apt install -qqy intellij-idea-ce  pycharm-community')
    # local('sudo apt install -qqy spotify discord signal')
    # local('sudo apt install -qqy ibus-cangjie')
    # local('sudo apt install -qqy ttf-emojione-color ttf-twemoji-color')
    # local('sudo apt install -qqy peek')
    # local('sudo apt install -qqy bitwarden')

    packages_list=[
        'gnome-shell-extension-tilix-dropdown', 'tilix',
        'vlc',
        'p7zip unrar tar rsync',
        'network-manager-openconnect network-manager-openvpn network-manager-pptp',
        'rhythmbox remmina',
        'rclone filezilla',
        'virtualbox virtualbox-dkms virtualbox-ext-pack',
        'tmux  imwheel htop nmap httpie vim',
        'net-tools'
    ]

    for package in packages_list:
        apt_install_package(package)


@task
def install_google_cloud_sdk():
    ubuntu_code_version=local('lsb_release -c -s',capture=True)
    CLOUD_SDK_REPO_ENV_VAR = 'cloud-sdk-{}'.format(ubuntu_code_version)
    
    # Add the Cloud SDK distribution URI as a package source
    local('echo "deb http://packages.cloud.google.com/apt {} main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list'.format(CLOUD_SDK_REPO_ENV_VAR))

    # Import the Google Cloud Platform public key
    local('curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -')

    # Update the package list and install the Cloud SDK
    local('sudo apt-get update && sudo apt-get install -qqy google-cloud-sdk')

@task
def install_gnome_ext():
    list_ext=[
        'gnome-shell-extensions',
        'gnome-shell-extension-dashtodock',
        'gnome-shell-pomodoro',
        'gnome-shell-extension-mediaplayer',
        'gnome-shell-extension-caffeine',
        'arc-theme'
        # 'gnome-shell-extension-no-topleft-hot-corner',
        # 'gnome-shell-extension-gsconnect',
        # 'gnome-shell-extension-topicons-plus',
        # 'gnome-shell-extension-no-title-bar',
        # 'gnome-shell-extension-extended-gestures'
    ]
    for ext in list_ext:
        apt_install_package(ext)

    local('sudo apt-get remove gnome-shell-extension-ubuntu-dock')
    local('gsettings set org.gnome.shell enable-hot-corners false')

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
    local('sudo apt install python3-pip')
    local('sudo pip3 install --upgrade pip')
    list_pip=['pipenv']
    results=[local('sudo pip3 install {}'.format(pip_pkg))  for pip_pkg in list_pip]
