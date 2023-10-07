#!/usr/bin/python3
""" a Fabric script (based on the file `3-deploy_web_static.py`) that
    deletes out-of-date archives, using the function `do_clean`
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


def do_clean(number=0):
    """ deletes out-of-date archives"""
    try:
        if int(number) < 0:
            return False
    except Exception:
        return False
    try:
        # local archive
        number = int(number)
        loc_rst = local("ls ./versions", capture=True)  # get the arcives
        loc_arc = loc_rst.stdout.splitlines()
        loc_lst = [element for element in loc_arc]  # store in a list
        loc_sort = sorted(loc_lst, key=lambda archive:  # sort DSC
                          archive.split("_")[2].split(".")[0], reverse=True)

        # web server archives
        web_rst = run("ls /data/web_static/releases/ | grep web_static")
        web_dir = web_rst.stdout.splitlines()
        web_list = [element for element in web_dir]
        web_sort = sorted(web_list, key=lambda
                          folder: folder.split("_")[2], reverse=True)

        if number == 0 or number == 1:  # list of items to delete ord by number
            del_arcs = loc_sort[number:]
            del_dirs = web_sort[number:]
        else:
            del_arcs = loc_sort[number:]
            del_dirs = web_sort[number:]

        for del_arc in del_arcs:  # delete archives locally
            local("rm -rf ./versions/{}".format(del_arc))

        for directory in del_dirs:  # delete directories remotely
            remote_path = "/data/web_static/releases/{}".format(directory)
            run("sudo rm -rf {}".format(remote_path))

        return True
    except Exception:
        return False
