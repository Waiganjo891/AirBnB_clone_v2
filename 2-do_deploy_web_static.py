#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers and deploy it.
"""
from fabric.api import env, put, run
import os

# Define web server IPs
env.hosts = ['100.26.214.182', '54.162.5.131']

def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.

    Args:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if all operations have been done correctly, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_folder = "/data/web_static/releases/{}/".format(
            archive_filename[:-4])
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, archive_folder))
        run("rm /tmp/{}".format(archive_filename))
        run("mv {}web_static/* {}".format(archive_folder, archive_folder))
        run("rm -rf {}web_static".format(archive_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(archive_folder))
        return True
    except Exception as e:
        return False
