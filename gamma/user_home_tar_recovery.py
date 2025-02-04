import os
import subprocess
import time

# 配置参数
ZFS_POOL = "gamma/home"

def extract_tar_to_zfs(tar_file, username):
    """将 tar 文件解压到 ZFS 分区"""
    zfs_dataset = f"{ZFS_POOL}/{username}"
    mount_point = f"."

    if not os.path.exists(mount_point):
        print(f"挂载点 {mount_point} 不存在，请先创建 ZFS 分区。")
        return False

    try:
        start_time = time.time()
        # 使用 tar 解压文件
        subprocess.run(
            ["tar", "--preserve-permissions","--hard-dereference", "--preserve-order", "--same-owner", "-xf", tar_file, "-C", mount_point],
            check=True
        )
        elapsed_time = time.time() - start_time
        print(f" 成功解压 {tar_file} 到 {mount_point}，耗时 {elapsed_time:.2f} 秒")
        return True
    except subprocess.CalledProcessError as e:
        print(f" 解压 {tar_file} 时发生错误: {e}")
        return False
    except Exception as e:
        print(f" 解压 {tar_file} 时发生未知错误: {e}")
        return False

def main():
    # 获取当前目录下的所有 tar 文件
    backup_files = [f for f in os.listdir(".") if f.count("backup_") != 0 and f.endswith(".tar")]

    if not backup_files:
        print("没有找到任何备份文件。")
        return

    total_files = len(backup_files)
    print(f"找到 {total_files} 个备份文件，需要解压。")

    for idx, backup_file in enumerate(backup_files, start=1):
        try:
            # 提取用户名
            username = backup_file.split("_")[0]
            print(f" [{idx}/{total_files}] 解压用户 {username} 的备份文件: {backup_file} ...")

            # 解压到 ZFS 分区
            start_time = time.time()
            success = extract_tar_to_zfs(backup_file, username)
            elapsed_time = time.time() - start_time

            if success:
                print(f"[{idx}/{total_files}] 用户 {username} 的备份文件已处理完成，总耗时 {elapsed_time:.2f} 秒")
            else:
                print(f"[{idx}/{total_files}] 用户 {username} 的备份文件处理失败")
        except Exception as e:
            print(f"[{idx}/{total_files}] 处理用户 {username} 的备份文件时发生错误: {e}")

if __name__ == "__main__":
    main()
