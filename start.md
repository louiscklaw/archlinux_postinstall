

apt-get install -qqy build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-dev


apt-get install -qqy python3-dev python3-pip

pip3 install --upgrade pip
pip3 install fabric3

apt-get install -qqy ssh
systemctl enable ssh 
systemctl start ssh

fab -H localhost install_vscode
