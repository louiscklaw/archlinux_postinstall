#!/usr/bin/env python3

import os
import sys

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.project import *
from fabric.contrib.files import *

from pprint import pprint

from common import *

"""
sudo apt install -qqy  git  fabric
git config --global user.email "logickee@gmail.com"
git config --global user.name "logickee"
git config --global core.editor "vim"

fallback_origional_gnome()
gnome_natural_scrolling()
install_pip()
install_cursor()
install_theme()
install_google_cloud_sdk()
install_vim()
install_docker()
install_new()
install_spotify()
install_sshrc()
install_zsh()
install_pycharm()
install_gterminal_theme()
"""


"""fab -f fab_gnome.py -H 192.168.88.246 bootstrap_git install_sshrc install_spotify install_utilities install_docker install_vim install_theme install_cursor bootstrap_vscode_settings gnome_natural_scrolling
"""



CWD = os.path.dirname(os.path.abspath(__file__))
PROJ_HOME = [
    CWD,
    '/home/logic/_tmp'
]

@task
def install_chinese():
    sudo('apt-get install -qqy ibus-table-cangjie3')

@task
def bootstrap_git():

    rsync_project(
        remote_dir=PROJ_HOME[1],
        local_dir=PROJ_HOME[0]+'/'
    )
    sudo('apt install -qqy  git ')
    run('git config --global user.email "logickee@gmail.com"')
    run('git config --global user.name "logickee"')
    run('git config --global core.editor "vim"')
    run('cat /dev/zero | ssh-keygen -q -N ""')

    run('mkdir -p {}'.format(PROJ_HOME[1]))


def get_lsbrelease():
    return run('lsb_release -c -s')

def apt_install_package(list_package):
    sudo('apt install -qqy {}'.format(list_package))



@task
def install_gterminal_theme():
    # https://github.com/Mayccoll/Gogh/blob/master/content/themes.md
    sudo('apt-get install -qqy dconf-cli')
    run('wget -O xt  http://git.io/v3D8e && chmod +x xt && ./xt && rm xt')

# @task
# def install_zsh():
#     apt_install_package('git zsh wget')
#     run('wget --no-check-certificate https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh')
#     sudo('chsh -s /usr/bin/zsh')


@task
def install_sshrc():
    run('wget --no-check-certificate https://raw.githubusercontent.com/Russell91/sshrc/master/sshrc')
    run('chmod +x sshrc')
    sudo('mv sshrc /usr/bin')

@task
def install_spotify():
    # 1. Add the Spotify repository signing keys to be able to verify downloaded packages
    # 2. Add the Spotify repository
    # 3. Update list of available packages
    # 4. Install Spotify
    sudo('apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0DF731E45CE24F27EEEB1450EFDC8610341D9410')
    # run('echo deb http://repository.spotify.com stable non-free | sudo tee /etc/apt/sources.list.d/spotify.list')
    run('echo deb http://repository.spotify.com stable non-free | sudo tee /etc/apt/sources.list.d/spotify.list')
    sudo('apt-get update')
    sudo('apt-get install -qqy spotify-client')

@task
def install_gitkraken():
    cmd = """wget https://release.gitkraken.com/linux/gitkraken-amd64.deb
    gdebi -n gitkraken-amd64.deb """
    send_commands_sudo_s(cmd)

@task
def install_rclone():
    # 'rclone',
    pass

@task
def install_utilities():
    # sudo('apt install -qqy meld nerd-fonts-complete monaco gitkraken')
    # sudo('apt install -qqy gedit-code-assistance editorconfig-gedit')
    # vdfuse
    # sudo('apt install -qqy android-studio genymotion scrcpy')
    # sudo('apt install -qqy discord signal')
    # sudo('apt install -qqy ibus-cangjie')
    # sudo('apt install -qqy peek')
    # sudo('apt install -qqy bitwarden')

    packages_list=[
        # 'tilix',
        'vlc',
        'p7zip unrar tar rsync',
        'network-manager-openconnect network-manager-openvpn network-manager-pptp',
        'rhythmbox remmina',
        'filezilla '
        'virtualbox virtualbox-dkms',
        'imwheel htop nmap httpie ',
        'net-tools'
    ]
    # virtualbox-ext-pack

    for package in packages_list:
        apt_install_package(package)

@task
def install_oh_my_tmux():
    run('rm -rf .tmux.conf')
    run('rm -rf ~/.tmux')
    run('git clone https://github.com/gpakosz/.tmux.git')
    run('ln -s -f .tmux/.tmux.conf . ')


@task
def install_rambox():
    cmd = """wget https://github.com/saenzramiro/rambox/releases/download/0.5.16/Rambox_0.5.16-x64.deb
    gdebi -n Rambox_0.5.16-x64.deb"""
    send_commands_sudo_s(cmd)

@task
def install_vim():
    sudo('apt install -qqy vim curl')
    run('curl https://j.mp/spf13-vim3 -L > spf13-vim.sh && sh spf13-vim.sh')

@task
def install_theme():
    # sudo('add-apt-repository ppa:noobslab/icons')
    cmd0="""
    add-apt-repository -y -u ppa:papirus/papirus
    apt-get update
    apt-get install -qqy papirus-icon-theme
    """
    cmd1="""    add-apt-repository -y -u  ppa:snwh/pulp
    add-apt-repository -y -u  ppa:noobslab/themes
    apt-get update
    apt-get install -qqy paper-icon-theme"""

    for cmd in [cmd0,cmd1]:
        send_commands(cmd)


@task
def install_cursor():
    sudo('rm -rf capitaine-cursors')
    run('git clone https://github.com/keeferrourke/capitaine-cursors.git')
    run('mkdir -p ~/.icons/capitaine-cursors')
    run('cp -pr capitaine-cursors/dist/ ~/.icons/capitaine-cursors')

@task
def inst1all_bootstrap_vscode_settings():
    setting_file='/home/logic/.config/Code/User/settings.json'
    run('mkdir -p {}'.format(os.path.dirname(setting_file)))
    # rsync_project(
    #     local_dir='/settings.json',
    #     remote_dir='/home/logic/.config/Code/User/settings.json'
    # )
    put(local_path='/home/logic/.config/Code/User', remote_path='/home/logic/.config/Code/User')

@task
def ins1tall_vscode():
    sudo('apt install -qqy curl')
    run('curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg')
    sudo('mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg')
    run('''sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list' ''')
    sudo('apt update')
    sudo('apt install -qqy code zeal')


@task
def install_powertop():
    cmd = """# install and configure TLP and PowerTOP
    apt-get install -qqy tlp tlp-rdw powertop
    tlp start
    # PowerTOP should be reporting a battery discharge rate of ~8-12W
    # powertop --auto-tune # auto-tune parameter will configure some recommended power-saving tweaks
    """
    for single_cmd in cmd.split('\n'):
        sudo(single_cmd)

@task
def install_pip():
    sudo('apt install -qqy python3-pip')
    sudo('pip3 install --upgrade pip')
    list_pip=['pipenv']
    results=[sudo('pip3 install {}'.format(pip_pkg))  for pip_pkg in list_pip]


@task
def install_php():
    sudo('apt-get install -qqy curl php-cli php-mbstring git unzip gdebi')
    sudo('curl -sS https://getcomposer.org/installer -o composer-setup.php')
    sudo('php composer-setup.php --install-dir=/usr/local/bin --filename=composer')


# @task
# def in1stall_gnome_ext():
#     list_ext = [
#         'gnome-shell-extension-no-topleft-hot-corner',
#         'gnome-shell-extension-gsconnect',
#         'gnome-shell-pomodoro',
#         'gtk-theme-arc-git',
#         'gnome-shell-extension-mediaplayer-git',
#         'gnome-shell-extension-topicons-plus',
#         'gnome-shell-extension-no-title-bar-git',
#         'gnome-shell-extension-caffeine-git',
#         'gnome-shell-extension-extended-gestures-git'
#     ]
#     for ext in list_ext:
#         local('pacaur -Sy --needed --noconfirm --noedit  {}'.format(ext))
#         local('id', capture=True)

@task
def install_vagrant():
    sudo('sudo apt-get install -qqy vagrant')



@task
def stop_error_reporting():
    cmd="""
    service apport stop
    apt purge -y apport
    """
    send_commands(cmd)

@task
def install_google_noto():
    cmd="""id
    wget -O Noto-hinted.zip https://noto-website-2.storage.googleapis.com/pkgs/Noto-hinted.zip
    unzip Noto-hinted.zip
    mkdir -p ~/.fonts
    cp *otf  ~/.fonts
    fc-cache -f -v # optional"""
    send_commands_sudo_s(cmd)

@task
def inst1all_android_studio():
    cmd ="""add-apt-repository -y -u ppa:maarten-fonville/android-studio
    apt-get update && apt install -qqy android-studio"""
    send_commands_sudo_s(cmd)

@task
def up_X201():
    install_list=[]

    for function_name in globals().keys():
        if function_name.find('install_') == 0:
            install_list.append(function_name)

    pprint(install_list)

    for install in install_list:
        eval("{}()".format(install))

@task
def sync_user_profile():
    local('rsync  -azh --exclude=trash --exclude=.cache --exclude=.git --progress ~/.zshrc {}:~'.format(env.hosts))
    local('rsync  -azh --exclude=trash --exclude=.cache --exclude=.git --progress ~/.tmux {}:~'.format(env.hosts))
    local('rsync  -azh --exclude=trash --exclude=.cache --exclude=.git --progress ~/.local {}:~'.format(env.hosts))
    local('rsync  -azh --exclude=trash --exclude=.cache --exclude=.git --progress ~/.config {}:~'.format(env.hosts))

    local('rsync  -azh --progress ~/_workspace {}:~'.format(env.hosts))


@task
def up_all():
    for function_name in globals().keys():
        if function_name.find('install_') == 0:
            print(function_name)
            eval("{}()".format(function_name))


def add_text_if_not_exit(filepath, text_to_check):
    if exists(filepath, use_sudo=False, verbose=False):
            if not contains(filepath, text_to_check, exact=False, use_sudo=False, escape=True, shell=False):
                append(filepath, text_to_check, use_sudo=False, partial=False, escape=True, shell=False)


@task
def install_autoenv():
    cmd = """git clone git://github.com/kennethreitz/autoenv.git ~/.autoenv"""
    local(cmd)
    ZSHRC_FILEPATH = '~/.zshrc'
    TEXT_TO_ADD_ZSHRC = 'source ~/.autoenv/activate.sh'

    add_text_if_not_exit(ZSHRC_FILEPATH, TEXT_TO_ADD_ZSHRC)

@task
def install_xnview():
    cmd="""sudo add-apt-repository -y -u ppa:dhor/myway
sudo apt-get update
sudo apt-get -qqy install xnview"""
    send_commands_sudo_s(cmd)
