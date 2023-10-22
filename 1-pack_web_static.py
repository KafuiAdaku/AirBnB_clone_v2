#!/usr/bin/python3
"""a Fabric script that generates a .tgz archive from the contents of the
`web_static` folder of your AirBnB Clone repo, using the function `do_pack`
"""
from fabric.api import *
from datetime import datetime


def do_pack():
    """genrates a `.tgz` file"""
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(time)
    archive_path = "versions/{}".format(archive_name)

    try:
        local("mkdir -p versions")
        local("tar  -czvf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None
