#!/usr/bin/env python3


from fabric.api import *



@task
def install_new():
    # oh-my-zsh sshrc
    local('sudo apt install -qqy zsh tmux  net-tools ')    
    local('sudo apt install -qqy zsh tmux  imwheel htop nmap httpie ')
    # local('sudo apt install -qqy meld nerd-fonts-complete monaco gitkraken')
    # local('sudo apt install -qqy gedit-code-assistance editorconfig-gedit')
    # local('sudo apt install -qqy linux linux-headers')
    # vdfuse
    local('sudo apt install -qqy virtualbox virtualbox-dkms virtualbox-ext-pack ')
    local('sudo apt install -qqy rclone filezilla')
    local('sudo apt install -qqy rhythmbox remmina')    
    # local('sudo apt install -qqy networkmanager-openconnect networkmanager-openvpn networkmanager-pptp')
    # local('sudo apt install -qqy google-cloud-sdk google-chrome')
    # local('sudo apt install -qqy android-studio genymotion scrcpy')
    # local('sudo apt install -qqy intellij-idea-ce  pycharm-community')
    # local('sudo apt install -qqy spotify discord signal')
    # local('sudo apt install -qqy ibus-cangjie')
    local('sudo apt install -qqy guake')
    # local('sudo apt install -qqy ttf-emojione-color ttf-twemoji-color')
    # local('sudo apt install -qqy peek')
    # local('sudo apt install -qqy bitwarden')
    local('sudo apt install -qqy vlc')
    local('sudo apt install -qqy p7zip unrar tar rsync')

@task
def install_gnome_ext():
    list_ext=[
        'plank',
        # 'gnome-shell-extension-no-topleft-hot-corner',
        # 'gnome-shell-extension-gsconnect',
        'gnome-shell-pomodoro',
        'gnome-shell-extension-mediaplayer',
        # 'gnome-shell-extension-topicons-plus',
        # 'gnome-shell-extension-no-title-bar',
        'gnome-shell-extension-caffeine',
        # 'gnome-shell-extension-extended-gestures'
    ]
    for ext in list_ext:
        local('sudo apt install -qqy  {}'.format(ext))

    local('sudo apt-get remove gnome-shell-extension-ubuntu-dock')
    local('gsettings set org.gnome.shell enable-hot-corners true')
    local('sudo apt install -qqy arc-theme')

@task
def install_vscode():
    local('sudo apt install -qqy curl')
    local('curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg')
    local('sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg')
    local('''sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list' ''')
    local('sudo apt update')
    local('sudo apt install code')


@task
def install_nvidia():
    local('sudo apt  install -qqy nvidia-384')

@task
def install_pip():
    local('sudo apt install python3-pip')
    local('sudo pip3 install --upgrade pip')
    list_pip=['pipenv']
    results=[local('sudo pip3 install {}'.format(pip_pkg))  for pip_pkg in list_pip]
