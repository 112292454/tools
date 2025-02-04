import subprocess
import os

# 配置参数
NFS_SERVER = "mainstorage.gamma.nginx.show"
MOUNT_BASE = "/home"
NFS_OPTIONS = "nfs4 rw,noatime,nodiratime,nofail,async,proto=tcp,sec=sys,local_lock=none 0 0"
FSTAB_FILE = "/etc/fstab"


def get_nfs_exports(nfs_server):
    """
    获取 NFS 服务器导出的路径
    """
    try:
        result = subprocess.run(
            ["showmount", "-e", nfs_server],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return [line.strip().removesuffix('*').strip() for line in result.stdout.splitlines()[1:]]  # 跳过第一行
    except subprocess.CalledProcessError as e:
        print(f"获取 NFS 导出路径时出错: {e.stderr}")
        return []


def read_fstab(fstab_file):
    """
    读取 /etc/fstab 文件内容
    """
    if os.path.exists(fstab_file):
        with open(fstab_file, "r") as f:
            return f.read().splitlines()
    return []


def write_fstab(fstab_file, lines):
    """
    将新的内容写入 /etc/fstab 文件
    """
    with open(fstab_file, "w") as f:
        f.write("\n".join(lines) + "\n")


def main():
    # 获取 NFS 导出路径
    exports = get_nfs_exports(NFS_SERVER)
    if not exports:
        print("未找到任何 NFS 导出路径。")
        return

    # 过滤出 /data/home 下的用户目录
    user_mounts = [
        export for export in exports if export.startswith("/data/home/") and export != "/data/home"
    ]

    if not user_mounts:
        print("未找到 /data/home 下的用户目录。")
        return

    print(f"发现以下用户目录需要挂载：{user_mounts}")

    # 获取当前的 /etc/fstab 内容
    current_fstab = read_fstab(FSTAB_FILE)

    # 存储新的 fstab 条目
    new_fstab = set(current_fstab)

    for user_mount in user_mounts:
        # 提取用户名
        user_name = user_mount.split("/")[-1]
        mount_point = f"{MOUNT_BASE}/{user_name}"

        # 确保挂载点存在
        os.makedirs(mount_point, exist_ok=True)

        # 构建 fstab 条目
        fstab_entry = f"{NFS_SERVER}:{user_mount} {mount_point} {NFS_OPTIONS}"

        # 检查是否已存在
        if fstab_entry not in current_fstab:
            new_fstab.add(fstab_entry)
            print(f"添加新的挂载: {fstab_entry}")
        else:
            print(f"跳过已存在的挂载: {fstab_entry}")

    # 写回 /etc/fstab
    write_fstab(FSTAB_FILE, sorted(new_fstab))
    print("✅ /etc/fstab 文件更新完成！")

    # 挂载所有新条目
    subprocess.run(["mount", "-a"], check=True)
    print("✅ 挂载已应用！")


if __name__ == "__main__":
    main()
