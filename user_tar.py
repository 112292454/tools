import os
import subprocess
import time
import logging
from datetime import datetime

# 设置home目录
HOME_DIR = '/home'
BACKUP_DIR = '/backup'
# 获取当前时间戳
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# 配置日志
logging.basicConfig(
    filename=f'backup_home_{timestamp}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 日志开始
logging.info("备份开始，当前时间戳: %s", timestamp)

# 遍历/home目录下的每个用户子目录
for user_dir in os.listdir(HOME_DIR):
    user_dir_path = os.path.join(HOME_DIR, user_dir)

    if os.path.isdir(user_dir_path):
        start_time = time.time()  # 记录打包开始时间

        # 获取用户的UID和GID
        try:
            user_info = subprocess.check_output(['getent', 'passwd', user_dir]).decode('utf-8').strip()
            user_uid = user_info.split(':')[2]
            user_gid = user_info.split(':')[3]
        except subprocess.CalledProcessError:
            #logging.warning("用户 %s 不存在，跳过", user_dir)
            #continue
            pass

        # 获取该用户目录的总大小（单位：字节）
        try:
            user_dir_size = subprocess.check_output(['du', '-sb', user_dir_path]).decode('utf-8').split()[0]
            user_dir_size = int(user_dir_size)  # 转换为整数
        except subprocess.CalledProcessError as e:
            logging.error("获取用户 %s 目录大小失败: %s", user_dir, e)
            continue
        size_gb= user_dir_size//1024//1024//1024
        logging.info("用户 %s 的目录大小: %d GB", user_dir, size_gb)
        if size_gb>1024:
            logging.info("用户 %s 的目录大小超过1TB，跳过", user_dir)
            continue


        # 打包该用户的目录，保留文件权限信息，不进行压缩
        tar_filename = f"{HOME_DIR}/{user_dir}_backup_{timestamp}.tar"
        try:
            subprocess.run(['tar', '-cpf', tar_filename, '-C', HOME_DIR, user_dir], check=True)
            end_time = time.time()  # 记录打包结束时间

            # 计算耗时
            elapsed_time = end_time - start_time

            # 日志记录打包信息
            logging.info("用户 %s 的目录已成功打包为 %s", user_dir, tar_filename)
            logging.info("用户 %s 打包耗时: %.2f 秒", user_dir, elapsed_time)

            # 将源文件夹移动到备份目录
            subprocess.run(['mv', user_dir_path, BACKUP_DIR], check=True)
            logging.info("用户 %s 的源目录已移动到 %s", user_dir, BACKUP_DIR)

        except subprocess.CalledProcessError as e:
            logging.error("打包用户 %s 目录时出错: %s", user_dir, e)

# 总结日志
logging.info("所有用户的目录已打包完成")