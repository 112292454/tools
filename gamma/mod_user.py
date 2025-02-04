from time import sleep

import paramiko
import os
import sys
import subprocess

# 目标服务器列表（可以包含当前机器的IP）
servers = [
    "a800.gamma.nginx.show",
    "3090.gamma.nginx.show",
    "2080.gamma.nginx.show",
]

# SSH 端口
ssh_port = 10090

# ZFS 配置
ZFS_POOL = "gamma/home"
RESERVED_SPACE = "100G"
HARD_LIMIT = "1T"


def create_zfs_partition(username):
    """创建 ZFS 分区并设置限额"""
    zfs_dataset = f"{ZFS_POOL}/{username}"
    mount_point = f"./{zfs_dataset}"

    # 创建 ZFS 分区
    subprocess.run(["zfs", "create", zfs_dataset], check=True)
    subprocess.run(["zfs", "set", f"refquota={HARD_LIMIT}", zfs_dataset], check=True)
    subprocess.run(["zfs", "set", f"reservation={RESERVED_SPACE}", zfs_dataset], check=True)
    subprocess.run(["chown", f"{username}:{username}", "-R", f"/data/home/{username}"], check=True)

    print(f"ZFS 分区 {zfs_dataset} 已创建，限额设置为 {HARD_LIMIT}，保留空间设置为 {RESERVED_SPACE}")


def share_zfs_pool():
    """共享 ZFS 存储池"""
    # 假设共享池的脚本是 zfs_export.py
    subprocess.run(["python3", "/root/zfs_export.py"], check=True)
    print("ZFS 存储池已共享。")


def mount_zfs_on_remote(server):
    """在远程服务器上挂载 ZFS 存储池"""
    # 假设远程挂载脚本是 zfs_client_mount.py
    subprocess.run(
        ["ssh", "-p", "10090", f"root@{server}", "python3.10", "/root/zfs_client_mount.py"],
        check=True
    )
    # subprocess.run(["ssh", "-p", "10090", f"root@{server}", "mount", "-a"],check=True)
    print(f"远程服务器 {server} 上已挂载 ZFS 存储池。")


def add_user_and_sync(username, password):
    # 在本机上添加用户
    os.system(f"adduser --disabled-password --gecos '' {username}")

    # 设置用户密码
    os.system(f"echo {username}:{password} | chpasswd")

    # 获取用户信息
    user_info = get_user_info(username)

    # 创建 ZFS 存储池并共享
    create_zfs_partition(username)
    share_zfs_pool()
    sleep(3)

    # 在本机同步成功后，将新用户信息同步到其他服务器
    for server in servers:
        print(f">同步用户 {username} 到服务器: {server}")
        sync_user_info_to_remote(server, user_info)

    # 挂载 ZFS 存储池到所有待同步的服务器
    for server in servers:
        print(f">为服务器 {server} 挂载 ZFS 存储池")
        mount_zfs_on_remote(server)


def delete_user_and_sync(username):
    # 从本机删除用户相关信息
    user_info = get_user_info(username)

    # 在本机删除用户
    os.system(f"userdel -r {username}")

    # 在本机同步删除操作后，删除远程服务器的用户信息
    for server in servers:
        if server == get_current_host():
            continue  # 跳过当前服务器
        print(f">删除用户 {username} 从服务器: {server}")
        delete_user_info_from_remote(server, user_info)


# 获取当前主机的名称
def get_current_host():
    return os.uname()[1]


# 获取用户在 /etc/passwd, /etc/shadow 和 /etc/group 中的行
def get_user_info(username):
    user_info = {}

    # 获取 /etc/passwd 信息
    with open("/etc/passwd", "r") as f:
        for line in f:
            if line.startswith(username + ":"):
                user_info["passwd"] = line
                break

    # 获取 /etc/shadow 信息
    with open("/etc/shadow", "r") as f:
        for line in f:
            if line.startswith(username + ":"):
                user_info["shadow"] = line
                break

    # 获取 /etc/group 信息
    with open("/etc/group", "r") as f:
        for line in f:
            if line.startswith(username + ":"):
                user_info["group"] = line
                break

    return user_info


# 使用 SSH 将用户信息同步到远程服务器
def sync_user_info_to_remote(server, user_info):
    # 使用 paramiko 连接到远程服务器
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动接受未知主机密钥
    try:
        ssh.connect(server, port=ssh_port, username="root")

        # 同步 /etc/passwd
        update_file_on_remote(ssh, "/etc/passwd", user_info["passwd"])

        # 同步 /etc/shadow
        update_file_on_remote(ssh, "/etc/shadow", user_info["shadow"])

        # 同步 /etc/group
        update_file_on_remote(ssh, "/etc/group", user_info["group"])

    finally:
        ssh.close()


# 使用 SSH 从远程服务器删除用户信息
def delete_user_info_from_remote(server, user_info):
    # 使用 paramiko 连接到远程服务器
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动接受未知主机密钥
    try:
        ssh.connect(server, port=ssh_port, username="root")

        # 从远程服务器删除用户信息
        remove_line_from_remote(ssh, "/etc/passwd", user_info["passwd"])
        remove_line_from_remote(ssh, "/etc/shadow", user_info["shadow"])
        remove_line_from_remote(ssh, "/etc/group", user_info["group"])

    finally:
        ssh.close()


import re

# 将文件内容添加到远程文件
def update_file_on_remote(ssh, remote_file, line_to_add):
    # 获取当前文件内容
    stdin, stdout, stderr = ssh.exec_command(f"cat {remote_file}")
    file_content = stdout.read().decode()

    # 如果是 /etc/shadow 文件，只比较用户名部分
    if remote_file == "/etc/shadow":
        username = line_to_add.split(":")[0]  # 获取用户名
        # 使用正则表达式检查文件中是否已经存在该用户名的记录
        # 确保匹配的用户名后面是冒号 (即 "username:")
        if not re.search(rf"^{username}:", file_content, re.MULTILINE):
            # 将用户信息追加到目标文件
            ssh.exec_command(f"echo '{line_to_add.strip()}' | tee -a {remote_file} > /dev/null")
            print(f">>成功同步 {remote_file} 文件。")
        else:
            print(f">>{remote_file} 中已存在该用户名，跳过同步。")
    else:
        # 对于其他文件，直接检查整行是否存在
        if line_to_add not in file_content:
            # 将用户信息追加到目标文件
            ssh.exec_command(f"echo '{line_to_add.strip()}' | tee -a {remote_file} > /dev/null")
            print(f">>成功同步 {remote_file} 文件。")
        else:
            print(f">>{remote_file} 中已存在该用户信息，跳过同步。")



# 从远程文件中删除指定行
def remove_line_from_remote(ssh, remote_file, line_to_remove):
    # 获取当前文件内容
    stdin, stdout, stderr = ssh.exec_command(f"cat {remote_file}")
    file_content = stdout.read().decode()

    # 检查文件中是否包含该行
    if line_to_remove in file_content:
        # 删除该行
        command = f"sed -i '/{line_to_remove.strip()}/d' {remote_file}"
        ssh.exec_command(command)
        print(f">>成功删除 {remote_file} 中的用户信息。")
    else:
        print(f">>{remote_file} 中未找到该用户信息，跳过删除。")


# 主程序入口
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python sync_user.py <操作> <用户名> [密码]")
        sys.exit(1)

    operation = sys.argv[1]
    username = sys.argv[2]

    if operation == "add" and len(sys.argv) == 4:
        password = sys.argv[3]
        add_user_and_sync(username, password)
    elif operation == "del":
        delete_user_and_sync(username)
    else:
        print("无效的操作或缺少参数。")
        sys.exit(1)
