#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers and deploy it.
"""
from fabric.api import env, put, run
import os

env.hosts = ['100.26.214.182', '54.162.5.131']
env.user = 'name'
env.key_filename = '/root/.ssh'


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
        put(archive_path, '/tmp/')
        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]
        run('mkdir -p /data/web_static/releases/{}'.format(archive_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(archive_filename, archive_name))
        run('rm /tmp/{}'.format(archive_filename))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(archive_name))
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", str(e))
        return False
