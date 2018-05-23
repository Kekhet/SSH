import os
import paramiko
import json
from pip._vendor.distlib.compat import raw_input


def update(local_folder, remote_path, local_path, ignore, sftp):
    for file in local_folder:
        if file in remote_folder:
            if file.split('.')[-1] not in ignore:
                sftp.put(local_path + '/' + file, remote_path + '/' + file)
                print("File updated: " + file)


def overwrite(local_folder, remote_path, local_path, ignore, sftp):
    for file in local_folder:
        if file.split('.')[-1] not in ignore:
            sftp.put(local_path + '/' + file, remote_path + '/' + file)
            print("File updated: " + file)


def add_non_existing(local_folder, remote_path, local_path, ignore, sftp):
    for file in local_folder:
        if file not in remote_folder:
            if file.split('.')[-1] not in ignore:
                sftp.put(local_path + '/' + file, remote_path + '/' + file)
                print("File updated: " + file)


with open("Config.json") as f:
    data = json.load(f)

hostname = data["server_address"]
port = data["port"]
username = data["username"]
password = raw_input("Password: ")
mode = data["mode"]
local_path = data["local_folder"]
remote_path = data["remote_folder"]
ignore = data["ignore"]

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    client.connect(hostname, port=port, username=username, password=password)
    sftp = client.open_sftp()

    local_folder = os.listdir(local_path)
    remote_folder = sftp.listdir(remote_path)

    print(local_folder)
    print(remote_folder)

    if mode == 'overwrite':
        overwrite(local_folder, remote_path, local_path, ignore, sftp)
    elif mode == 'update':
        update(local_folder, remote_path, local_path, ignore, sftp)
    elif mode == 'add_non_existing':
        add_non_existing(local_folder, remote_path, local_path, ignore, sftp)
    print(sftp.listdir(remote_path))
finally:
    client.close()

