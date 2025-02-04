import sys

from base_env import *
import media.hash as myHash
# 调用这个文件时，应当根据命令行输入的path参数，计算其中所有文件的hash值，然后append到当前文件夹下的garbage_hash.json文件中

def calc_hash(path):
    # 计算文件夹下所有文件的hash值
    hash_dict = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            fingerprint = myHash.generate_fingerprint(file_path)
            hash_dict[fingerprint['naive_hash']['value']] = fingerprint
    # touch garbage_hash.json
    if not os.path.exists("garbage_hash.json"):
        with open("garbage_hash.json", "w",encoding='utf-8') as f:
            json.dump({}, f)
    # 将hash值写入文件
    with open("garbage_hash.json", "r",encoding='utf-8') as f:
        garbage_hash:dict = json.load(f)
    garbage_hash.update(hash_dict)
    with open("garbage_hash.json", "w",encoding='utf-8') as f:
        json.dump(garbage_hash, f,indent=4,ensure_ascii=False)

if __name__ == "__main__":
    path = sys.argv[1]
    calc_hash(path)