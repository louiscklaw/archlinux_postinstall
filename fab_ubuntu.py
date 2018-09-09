#!/usr/bin/env python

from common import *

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.project import *

TMP_DIR = '/tmp'
NO_SUCH_FILE_OR_DIRECTORY = 'No such file or directory'


def apt_add_repository(ppa_address):
    ppa_address = ppa_address.strip()
    sudo('add-apt-repository -y -u {}'.format(ppa_address))

def apt_install_package(list_package):
    sudo('apt install -y {}'.format(' '.join(list_package)))


def download_file(url, save_to_file):
    wget_command = 'wget -O {} {}'.format(save_to_file, url)
    sudo(wget_command)


def check_file_exist(file_to_check):
    found = False
    with settings(warn_only=True):
        print('download iso file')
        result = sudo('ls -1 {}'.format(file_to_check))
        if result.find(NO_SUCH_FILE_OR_DIRECTORY) > -1:
            pass
        else:
            found = True

    return found


def get_dd_cmd(iso_file, dev_path):
    dd_cmd = 'dd if={} of={}'.format(iso_file, dev_path)
    return dd_cmd


def unmount_device(dev_path):
    with settings(warn_only=True):
        sudo('umount {}'.format(dev_path))


def dd_iso_to_usb(iso_file, dev_path):
    dd_cmd = get_dd_cmd(iso_file, dev_path)
    sudo(dd_cmd)


def mkdir_boot_usb(ubuntu_iso_temp, ubuntu_iso_url, device_path):
    with cd(TMP_DIR):
        dd_cmd = get_dd_cmd(ubuntu_iso_temp, device_path)

        keep_going = prompt('the dd command is going to be: {}, press "y" to continue? '.format(dd_cmd), default='n')
        if keep_going == 'y':
            if check_file_exist(ubuntu_iso_temp):
                print('{} found, skip download... '.format(ubuntu_iso_temp))
            else:
                download_file(ubuntu_iso_url, ubuntu_iso_temp)
            unmount_device(device_path)
            dd_iso_to_usb(ubuntu_iso_temp, device_path)


class ubuntu_1804:
    UBUNTU_ISO_FILENAME = 'ubuntu-18.04-desktop-amd64.iso'
    UBUNTU_ISO_URL = 'http://ftp.cuhk.edu.hk/pub/Linux/ubuntu-releases/18.04/' + UBUNTU_ISO_FILENAME
    UBUNTU_ISO_TEMP = os.path.join(TMP_DIR, UBUNTU_ISO_FILENAME)

    def mkdir_boot_sub(device_path):
        mkdir_boot_usb(ubuntu_1804.UBUNTU_ISO_FILENAME, ubuntu_1804.UBUNTU_ISO_URL, device_path)


class ubuntu_1604:
    UBUNTU_ISO_FILENAME = 'ubuntu-gnome-16.04.4-desktop-amd64.iso'
    UBUNTU_ISO_URL = 'http://cdimage.ubuntu.com/ubuntu-gnome/releases/16.04/release/' + UBUNTU_ISO_FILENAME
    UBUNTU_ISO_TEMP = os.path.join(TMP_DIR, UBUNTU_ISO_FILENAME)

    def mkdir_boot_sub(device_path):
        mkdir_boot_usb(ubuntu_1604.UBUNTU_ISO_FILENAME, ubuntu_1604.UBUNTU_ISO_URL, device_path)


@task
def make_1804_usb(device_path):
    ubuntu_1804.mkdir_boot_sub(device_path)


@task
def make_1604_usb(device_path):
    ubuntu_1604.mkdir_boot_sub(device_path)


@task
def ubuntu_1804_after_install():
    # Things To Do After Installing Ubuntu 18.04 (Bionic Beaver)
    sudo('apt update && apt -qqy upgrade')
    sudo('sudo apt install -qqy ubuntu-restricted-extras')

    # 8. Install TLP and Disable Automatic Suspend
    sudo('apt install -qqy tlp tlp-rdw')


@task
def install_insomnia():
    sudo('echo "deb https://dl.bintray.com/getinsomnia/Insomnia /" | sudo tee -a /etc/apt/sources.list.d/insomnia.list')
    sudo('wget --quiet -O - https://insomnia.rest/keys/debian-public.key.asc | sudo apt-key add - ')
    sudo('apt update && apt install -qqy insomnia ')


@task
def install_utilities():
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

    packages_list = [
        'vlc',
        'browser-plugin-vlc',
        'p7zip',
        'unrar',
        'tar',
        'rsync',
        'network-manager-openconnect',
        'network-manager-openvpn',
        'network-manager-pptp',
        'rhythmbox',
        'remmina',
        'filezilla',
        'virtualbox',
        'virtualbox-dkms ',
        'tmux',
        'imwheel',
        'htop',
        'nmap',
        'httpie',
        'vim',
        'net-tools',
        'tilix','gnome-shell-extension-tilix-dropdown',
        'ack','entr',
        'python','python3',
        # 'python-pip','python3-pip',
        'gnome-tweaks',
        'glances',
        'flameshot',
        'gdebi','dconf-editor',
        'baobab','bleachbit','gigolo'

    ]
    for package in packages_list:
        apt_install_package([package])

def gdebi_from_url(url):
    sudo('apt install -qqy gdebi')
    sudo('wget -O /tmp/temp.deb {}'.format(url))
    sudo('gdebi -q -n /tmp/temp.deb')


@task
def install_cronopete():
    CRONOPETE_DEB = '/tmp/cronpoete.deb'
    DEB_DOWNLOAD_URL = 'http://www.rastersoft.com/descargas/cronopete/cronopete-bionic_4.5.1-ubuntu1_amd64.deb'

    apt_install_package(['gigolo'])

    wget_command = 'wget -O {} {}'.format(CRONOPETE_DEB, DEB_DOWNLOAD_URL)
    sudo(wget_command)
    sudo('gdebi -n -q  {}'.format(CRONOPETE_DEB))


@task
def install_sendanywhere():
    gdebi_from_url('https://update.send-anywhere.com/linux_downloads/sendanywhere_latest_amd64.deb')

@task
def install_vim():
    sudo('rm -rf ~/.spf13-vim-3')
    sudo('apt install -qqy vim curl git')
    run('curl https://j.mp/spf13-vim3 -L > spf13-vim.sh && sh spf13-vim.sh')


@task
def install_cursor():
    sudo('rm -rf capitaine-cursors')
    sudo('add-apt-repository -y -u ppa:dyatlov-igor/la-capitaine')
    sudo('apt install -y la-capitaine-cursor-theme')


@task
def install_powertop():
    cmd = """# install and configure TLP and PowerTOP
    apt-get install -qqy tlp tlp-rdw powertop
    tlp start
    # PowerTOP should be reporting a battery discharge rate of ~8-12W
    # powertop --auto-tune # auto-tune parameter will configure some recommended power-saving
    """
    for single_cmd in cmd.split('\n'):
        sudo(single_cmd)


@task
def install_pip():
    sudo('apt install -qqy python3-pip')
    sudo('pip3 install --upgrade pip')
    list_pip = ['pipenv']
    results = [sudo('pip3 install {}'.format(pip_pkg)) for pip_pkg in list_pip]


@task
def install_php():
    sudo('apt-get install -qqy curl php-cli php-mbstring git unzip gdebi')
    sudo('curl -sS https://getcomposer.org/installer -o composer-setup.php')
    sudo('php composer-setup.php --install-dir=/usr/local/bin --filename=composer')


@task
def install_vagrant():
    sudo('apt-get install -qqy vagrant')

@task
def install_git():
    apt_install_package(['git'])
    local('git config --global core.editor "vim"')


@task
def stop_error_reporting():
    cmd = """service apport stop && apt purge -y apport"""
    with settings(warn_only=True):
        send_commands_sudo_s(cmd)


@task
def install_google_noto():
    cmd = """id
    wget -O Noto-hinted.zip https://noto-website-2.storage.googleapis.com/pkgs/Noto-hinted.zip
    unzip Noto-hinted.zip
    mkdir -p ~/.fonts
    cp *otf  ~/.fonts
    fc-cache -f -v # optional"""
    send_commands_sudo_s(cmd)


@task
def install_android_studio():
    cmd = """sudo add-apt-repository -y -u ppa:maarten-fonville/android-studio
    apt-get update
    apt install -qqy android-studio"""
    send_commands_sudo_s(cmd)


@task
def install_autoenv():
    cmd = """git clone git://github.com/kennethreitz/autoenv.git ~/.autoenv"""
    local(cmd)
    ZSHRC_FILEPATH = '~/.zshrc'
    TEXT_TO_ADD_ZSHRC = 'source ~/.autoenv/activate.sh'

    add_text_if_not_exit(ZSHRC_FILEPATH, TEXT_TO_ADD_ZSHRC)


@task
def install_jetbrain():
    cmd = """curl -s https://s3.eu-central-1.amazonaws.com/jetbrains-ppa/0xA6E8698A.pub.asc | sudo apt-key add -
echo "deb http://jetbrains-ppa.s3-website.eu-central-1.amazonaws.com bionic main" | sudo tee /etc/apt/sources.list.d/jetbrains-ppa.list > /dev/null
sudo apt-get update
sudo apt-get -qqy install intellij-idea-community
sudo apt-get -qqy install phpstorm
sudo apt-get -qqy install pycharm-community
sudo apt-get -qqy install goland
sudo apt-get -qqy install webstorm
sudo apt-get -qqy install clion
sudo apt-get -qqy install datagrip
"""
    with cd('/tmp'):
        sudo('apt-get install -qqy curl')
        sudo(cmd)


@task
def install_spotify():
    # 1. Add the Spotify repository signing keys to be able to verify downloaded packages
    # 2. Add the Spotify repository
    # 3. Update list of available packages
    # 4. Install Spotify
    local('echo deb http://repository.spotify.com stable non-free | sudo tee /etc/apt/sources.list.d/spotify.list')
    sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A87FF9DF48BF1C90')
    sudo('apt-get update')
    sudo('apt-get install -qqy spotify-client')


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
def install_vscode():
    cmd = """apt install -qqy curl wget
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
    mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
    sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
    apt update
    apt install -qqy code zeal
    wget -O ~/vsls-reqs https://aka.ms/vsls-linux-prereq-script && bash ~/vsls-reqs"""
    send_commands_sudo_s(cmd)


@task
def install_gnome_ext():
    list_ext = [
        'arc-theme',
        'gnome-shell-extension-appindicator',
        'gnome-shell-extension-autohidetopbar',
        'gnome-shell-extension-better-volume',
        'gnome-shell-extension-caffeine',
        'gnome-shell-extension-dashtodock',
        'gnome-shell-extension-hard-disk-led',
        'gnome-shell-extension-hide-activities',
        'gnome-shell-extension-mediaplayer',
        'gnome-shell-extension-pixelsaver',
        'gnome-shell-extension-remove-dropdown-arrows',
        'gnome-shell-extension-tilix-dropdown',
        'gnome-shell-extension-tilix-shortcut',
        'gnome-shell-extension-top-icons-plus',
        'gnome-shell-extensions-gpaste',
        'gnome-shell-extensions',
        'gnome-shell-pomodoro',
        # 'gnome-shell-extension-no-topleft-hot-corner',
        # 'gnome-shell-extension-gsconnect',
        # 'gnome-shell-extension-topicons-plus',
        # 'gnome-shell-extension-no-title-bar',
        # 'gnome-shell-extension-extended-gestures'
    ]
    apt_install_package(list_ext)

    sudo('apt-get remove gnome-shell-extension-ubuntu-dock')
    # sudo('gsettings set org.gnome.shell enable-hot-corners false')
    run('gsettings set org.gnome.shell enable-hot-corners false')


@task
def install_synergy():
    apt_install_package(['synergy','sni-qt'])


@task
def install_google_cloud_sdk():
    ubuntu_code_version = local('lsb_release -c -s', capture=True)
    CLOUD_SDK_REPO_ENV_VAR = 'cloud-sdk-{}'.format(ubuntu_code_version)

    # Add the Cloud SDK distribution URI as a package source
    sudo('echo "deb http://packages.cloud.google.com/apt {} main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list'.format(CLOUD_SDK_REPO_ENV_VAR))

    # Import the Google Cloud Platform public key
    sudo('curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -')

    # Update the package list and install the Cloud SDK
    sudo('apt-get update && apt-get install -qqy google-cloud-sdk')


@task
def install_zsh():
    apt_install_package(['git', 'zsh', 'wget', 'zsh-syntax-highlighting'])
    with settings(warn_only=True):
        sudo('rm -rf /home/logic/.oh-my-zsh')
    run('wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh')
    sudo('chsh -s `which zsh` logic')


@task
def install_zsh_theme():
    cmd = """rm -rf /home/logic/.oh-my-zsh/custom/themes/spaceship-prompt
    git clone https://github.com/denysdovhan/spaceship-prompt.git "/home/logic/.oh-my-zsh/custom/themes/spaceship-prompt"
    ln -s "/home/logic/.oh-my-zsh/custom/themes/spaceship-prompt/spaceship.zsh-theme" "/home/logic/.oh-my-zsh/custom/themes/spaceship.zsh-theme" """
    with settings(warn_only=True):
        send_commands_sudo_s(cmd)

def install_paper_icon():
    cmd = '''add-apt-repository -y -u ppa:snwh/ppa && apt-get install paper-icon-theme'''
    with settings(warn_only):
        sudo(cmd)

@task
def install_material_theme():
    sudo('apt install -qqy materia-gtk-theme')


@task
def install_keybase():
    gdebi_from_url('https://prerelease.keybase.io/keybase_amd64.deb')
    local('run_keybase')

@task
def install_freecad():
    apt_add_repository('ppa:freecad-maintainers/freecad-stable')
    apt_install_package(['freecad'])
    local()

@task
def install_kicad():
    apt_add_repository('ppa:js-reynaud/kicad-5')
    apt_install_package('kicad kicad-demo kicad-libraries'.split(' '))

@task
def install_flatremix():
    apt_add_repository('ppa:daniruiz/flat-remix')
    apt_install_package('flat-remix flat-remix-gtk flat-remix-gnome'.split(' '))

@task
def install_all():
    # install_docker()
    sudo('apt clean')
    stop_error_reporting()
    ubuntu_1804_after_install()
    install_zsh()
    install_zsh_theme()
    install_vim()
    install_utilities()
    # install_insomnia()
    install_spotify()
    install_jetbrain()
    install_autoenv()
    # install_android_studio()

    install_vagrant()
    install_php()
    install_powertop()
    install_vscode()
    install_gnome_ext()
    install_google_cloud_sdk()

    sudo('apt-get autoclean')


    install_google_noto()
