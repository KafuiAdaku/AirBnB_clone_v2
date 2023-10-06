#!/usr/bin/python3
"""A Fabric script (based on the file 2-do_deploy_web_static.py) that creates
    and distributes an archive to your web servers, using the function deploy
"""
from fabric.api import *
from datetime import datetime
import os.path


env.hosts = ["100.24.205.66", "100.26.57.118"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """genrates a `.tgz` file"""
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(time)
    archive_path = "versions/{}".format(archive_name)

    try:
        local("mkdir -p versions")
        local("tar  -czf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """distributes an archive to specified  web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # get file name from path
        file_name = os.path.basename(archive_path).split(".")[0]

        # upload archive to the web server(s)
        put(archive_path, "/tmp/")

        # create directories
        run("sudo mkdir  -p /data/web_static/releases/{}".format(file_name))

        # uncompress archive
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}".
            format(file_name + ".tgz", file_name))

        # remove archive from /tmp
        run("sudo rm /tmp/{}".format(file_name + ".tgz"))

        # move contents to host's web_static
        run("sudo cp -R /data/web_static/releases/{}/web_static/* \
/data/web_static/releases/{}/".format(file_name, file_name))

        # remove excesses
        run("sudo rm -rf /data/web_static/releases/{}/web_static".
            format(file_name))

        # remove symbolic  link
        run("sudo rm -rf /data/web_static/current")

        # create new symbolic link
        run("sudo ln -sf /data/web_static/releases/{}/ \
/data/web_static/current".format(file_name))

        return True
    except Exception:
        return False

def deploy():
    """creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
