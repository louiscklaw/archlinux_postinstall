#!/usr/bin/env python3


from fabric.api import *
from common import *
from fabric.contrib.files import *

#   git config --global user.email "logickee@gmail.com"
#   git config --global user.name "logickee"

# sudo apt install -qqy  git python3-pip




def apt_install_package(list_package):
    sudo('apt install -qqy {}'.format(' '.join(list_package)))

@task
def install_pycharm():
    cmd = """id
    apt install -qqy gdebi
    id #
    wget https://launchpad.net/~viktor-krivak/+archive/ubuntu/pycharm/+files/pycharm_2018.1.1-1~xenial_amd64.deb
    gdebi -n pycharm_2018.1.1-1~xenial_amd64.deb"""
    with cd('/tmp'):
        send_commands_sudo_s(cmd)

@task
def install_intellj_idea():
    cmd="""id
    apt-add-repository -y -u ppa:mmk2410/intellij-idea
    apt-get update
    apt-get install -qqy intellij-idea-community
    """
    send_commands_sudo_s(cmd)

@task
def install_zsh():
    apt_install_package(['git', 'zsh','wget', 'zsh-syntax-highlighting'])
    run('wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh')
    sudo('chsh -s `which zsh` logic')


@task
def install_zsh_theme():
    cmd = """git clone https://github.com/denysdovhan/spaceship-prompt.git "/home/logic/.oh-my-zsh/custom/themes/spaceship-prompt"
    ln -s "/home/logic/.oh-my-zsh/custom/themes/spaceship-prompt/spaceship.zsh-theme" "/home/logic/.oh-my-zsh/custom/themes/spaceship.zsh-theme"
    """
    send_commands(cmd)

@task
def install_new():
    # local('sudo apt install -qqy meld nerd-fonts-complete monaco gitkraken')
    # local('sudo apt install -qqy gedit-code-assistance editorconfig-gedit')
    # local('sudo apt install -qqy linux linux-headers')
    # vdfuse
    # local('sudo apt install -qqy android-studio genymotion scrcpy')
    # local('sudo apt install -qqy intellij-idea-ce  pycharm-community')
    # local('sudo apt install -qqy spotify discord signal')
    # local('sudo apt install -qqy ibus-cangjie')
    # local('sudo apt install -qqy peek')
    # local('sudo apt install -qqy bitwarden')

    packages_list=[
        # 'tilix',
        'vlc browser-plugin-vlc',
        'p7zip unrar tar rsync',
        'network-manager-openconnect network-manager-openvpn network-manager-pptp',
        'rhythmbox remmina',
        # 'rclone',
        'filezilla',
        'virtualbox virtualbox-dkms ',
        'tmux  imwheel htop nmap httpie vim',
        'net-tools'
    ]

    apt_install_package(packages_list)


@task
def install_google_cloud_sdk():
    ubuntu_code_version=local('lsb_release -c -s',capture=True)
    CLOUD_SDK_REPO_ENV_VAR = 'cloud-sdk-{}'.format(ubuntu_code_version)

    # Add the Cloud SDK distribution URI as a package source
    sudo('echo "deb http://packages.cloud.google.com/apt {} main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list'.format(CLOUD_SDK_REPO_ENV_VAR))

    # Import the Google Cloud Platform public key
    sudo('curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -')

    # Update the package list and install the Cloud SDK
    sudo('apt-get update && apt-get install -qqy google-cloud-sdk')

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
    apt_install_package(list_ext)

    sudo('apt-get remove gnome-shell-extension-ubuntu-dock')
    # sudo('gsettings set org.gnome.shell enable-hot-corners false')


@task
def in1stall_gnome_ext():
    list_ext=[
        # 'gnome-shell-extension-autohidetopbar',
        # 'gnome-shell-extension-caffeine',
        # 'gnome-shell-extension-impatience',
        # 'gnome-shell-extension-mediaplayer',
        'gnome-shell-extensions-gpaste',
        # 'gnome-shell-extension-system-monitor',
        # 'gnome-shell-extension-tilix-dropdown',
        # 'gnome-shell-extension-top-icons-plus',
        # 'gnome-tweaks',
        # 'gnome-tweak-tool',
    ]
    for ext in list_ext:
        apt_install_package(ext)

    # sudo('apt-get remove gnome-shell-extension-ubuntu-dock
    run('gsettings set org.gnome.shell enable-hot-corners false')


@task
def install_vscode():
    cmd="""apt install -qqy curl
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
    mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
    sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
    apt update
    apt install -qqy code zeal"""
    send_commands(cmd)


@task
def install_nvidia():
    cmd = """add-apt-repository -y -u ppa:graphics-drivers/ppa
    apt update
    apt-get install -qqy nvidia-384
    apt-mark hold nvidia-384 # stop this package being auto-updated during package resolution
    # test that the nvidia drivers are working: nvidia-smi should output some GPU stats
    nvidia-smi
    # install Nvidia Prime: so we can disable the dedicated GPU when we don't want it
    apt-get install -qqy nvidia-prime
    prime-select intel
    """
    send_commands(cmd)

@task
def install_pip():
    cmd = """apt install -qqy python3-pip && pip3 install --upgrade pip"""
    send_commands(cmd)
    list_pip=['pipenv']
    results=[sudo('pip3 install {}'.format(pip_pkg))  for pip_pkg in list_pip]



@task
def inst1all_nvidia():
    sudo('apt  install -qqy nvidia-384')

def ensure_line_exist(filename, text_to_ensure):

    if not exists(filename, use_sudo=True, verbose=False):
        sudo('touch {}'.format(filename))

    if not contains(filename, text_to_ensure, exact=False, use_sudo=True, escape=True, shell=False, case_sensitive=True):
        append(filename, text_to_ensure, use_sudo=True, partial=False, escape=True, shell=False)


@task
def install_docker():
    sudo('apt install -qqy apt-transport-https ca-certificates curl software-properties-common')

    filename='/etc/apt/sources.list.d/docker.list'
    text='deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable'
    ensure_line_exist(filename, text)

    sudo('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -u -')
    sudo('apt update')
    sudo('apt install -qqy docker-ce')

    sudo('docker --version')

    sudo('usermod -a -G docker logic')

@task
def install_docker_compose():
    sudo('curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose')
    sudo('chmod +x /usr/local/bin/docker-compose')
    sudo('docker-compose --version')
