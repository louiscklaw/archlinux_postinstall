# init_py_dont_write_bytecode

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.project import *


import multiprocessing
total_cpu_threads = multiprocessing.cpu_count()


def threaded_local(command):
    sudo(command, capture=True)

def send_sudo_command(commands):
    sudo(commands.replace('\r\n', "&&"))

@task
def spin_go_env():

    commands="""add-apt-repository -y -u ppa:gophers/archive
apt-get update
apt-get install -qqy golang-1.10-go"""



@task
def spin_mongod():
    commands="""sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
    apt-get update
    apt-get install -qqy mongodb-org"""
    send_sudo_command(commands)
