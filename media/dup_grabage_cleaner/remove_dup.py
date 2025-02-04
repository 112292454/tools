import sys

import media.hash as myHash
from base_env import *


# 调用这个文件时，应当根据命令行输入的path参数，计算其中所有文件的hash值，过程中与garbage_hash.json文件中的hash值进行比对，如果hash值匹配（任一方法的），则直接删除文件
def remove_dup(path):
    # 读取garbage_hash.json
    if not os.path.exists("garbage_hash.json"):
        print("garbage_hash.json文件不存在")
        return
    with open("garbage_hash.json", "r", encoding='utf-8') as f:
        garbage_hash: dict = json.load(f)
    # 首先得到哈希表中最大文件的大小，然后再遍历时，只计算小于这个大小的文件的哈希值（因为target可能有大文件，哈希计算时间较长）
    max_size = 0
    for key in garbage_hash:
        file_size = garbage_hash[key]['file_size']
        size=float(file_size.split(' ')[0])
        # file_size结尾可能是以KB和MB为单位的，转换成B比较
        if garbage_hash[key]['file_size'].endswith('KB'):
            size *= 1024
        elif garbage_hash[key]['file_size'].endswith('MB'):
            size *= 1024 * 1024
        max_size = max(max_size, size)

    # 计算文件夹下所有文件的hash值
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            # 如果文件大小大于哈希表中最大文件的大小，则跳过
            if os.path.getsize(file_path) > max_size:
                print(f"SKIP:\t文件大小超过哈希表中最大文件的大小，跳过:\t{file_path}")
                continue
            fingerprint = myHash.generate_fingerprint(file_path)
            if fingerprint['naive_hash']['value'] in garbage_hash.keys():
                os.remove(file_path)
                print(f"DUP:\t发现重复文件,已删除：\t{file_path}")
            # todo: elif other methods


if __name__ == "__main__":
    path = sys.argv[1]
    remove_dup(path)
