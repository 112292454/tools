import os
import subprocess

# 配置参数
ZFS_POOL = "gamma/home"
RESERVED_SPACE = "100G"
# SOFT_LIMIT = "1T"
HARD_LIMIT = "1T"


def create_zfs_partition(username):
    """创建 ZFS 分区并设置限额"""
    zfs_dataset = f"{ZFS_POOL}/{username}"
    mount_point = f"./{zfs_dataset}"

    # 创建 ZFS 分区
    subprocess.run(["zfs", "create", zfs_dataset], check=True)
    subprocess.run(["zfs", "set", f"refquota={HARD_LIMIT}", zfs_dataset], check=True)
    subprocess.run(["zfs", "set", f"reservation={RESERVED_SPACE}", zfs_dataset], check=True)

    # 确保挂载点存在
    # if not os.path.exists(mount_point):
    #     os.makedirs(mount_point)

    return mount_point


def main():
    # 获取当前目录下的所有 tar 文件
    backup_files = [f for f in os.listdir(".") if f.count("backup_")!=0 and f.endswith(".tar")]

    if not backup_files:
        print("没有找到任何备份文件。")
        return

    for backup_file in backup_files:
        try:
            # 提取用户名
            username = backup_file.split("_")[0]
            print(f"创建用户 {username} 的 ZFS 分区...")

            # 创建 ZFS 分区
            mount_point = create_zfs_partition(username)
            print(f"ZFS 分区已创建并挂载到: {mount_point}")

        except subprocess.CalledProcessError as e:
            print(f"创建用户 {username} 的分区时发生错误: {e}")
        except Exception as e:
            print(f"创建用户 {username} 的分区时发生未知错误: {e}")


if __name__ == "__main__":
    main()
