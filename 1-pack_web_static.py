#!/usr/bin/python3
"""
Fabric script to generate tgz archive
execute: fab -f 1-pack_web_static.py do-pack
"""
from datetime import datetime
from fabric.api import *
import os


def do_pack():
    """
    making an archive on web_static folder
    """
    local('sudo mkdir -p versions')
    t = datetime.now()
    t_str = t.strftime('%Y%m%d%H%M%S')
    local(f'sudo tar -cvzf versions/web_static_{t_str}.tgz web_static')
    f_path = f"versions/web_static_{t_str}.tgz"
    f_size = os.path.getsize(f_path)
    print(f"web_static packed: {f_path} -> {f_size}Bytes")
