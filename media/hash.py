import base64
import hashlib
from io import BytesIO

import imagehash
# import numpy as np
# import torch
from PIL import Image
# from torchvision import models, transforms

from base_env import *
Image.MAX_IMAGE_PIXELS = 65536*65536  # 设置为合适的较大值


# 1. pHash 方法
def generate_phash(file_data):
    """
    生成文件的 pHash 指纹（感知哈希）。

    :param file_data: 文件数据（支持文件路径或字节流）
    :return: pHash 指纹字符串
    """
    image = Image.open(file_data)
    phash = imagehash.phash(image)
    return str(phash)


# 2. 朴素哈希方法
def generate_naive_hash(file_path, algorithm='sha256'):
    """
    生成文件的朴素哈希指纹。

    :param file_path: 文件数据（支持文件路径或字节流）
    :param algorithm: 哈希算法，默认为 'sha256'
    :return: 哈希指纹字符串
    """
    hash_func = getattr(hashlib, algorithm)()

    if isinstance(file_path, str):  # 如果是文件路径
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
    else:  # 如果是字节流
        hash_func.update(file_path)

    return hash_func.hexdigest(),algorithm


# 3. 基于 AI 的特征向量方法
# def generate_ai_fingerprint(file_data):
#     """
#     生成文件的 AI 指纹，并进行降维，将向量转换为字符串形式。
#
#     :param file_data: 文件数据（支持文件路径或字节流）
#     :param n_components: 降维后的向量长度
#     :return: AI 指纹字符串
#     """
#     # 使用预训练的 ResNet 模型提取特征
#     model = models.resnet50(pretrained=True)
#     model.eval()
#
#     preprocess = transforms.Compose([
#         transforms.Resize((224, 224)),
#         transforms.ToTensor(),
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#     ])
#     # 定义线性降维层
#     linear = torch.nn.Linear(1000, 128)
#
#
#     if isinstance(file_data, str):
#         image = Image.open(file_data).convert('RGB')
#     else:
#         image = Image.open(BytesIO(file_data)).convert('RGB')
#
#     input_tensor = preprocess(image).unsqueeze(0)  # 添加 batch 维度
#     with torch.no_grad():
#         features = model(input_tensor)
#         features = linear(features).squeeze().numpy()
#
#     # 将向量转换为 base64 编码的字符串
#     feature_bytes = features.astype(np.float32).tobytes()  # 转换为字节
#     feature_str = base64.b64encode(feature_bytes).decode('utf-8')  # Base64 编码为字符串
#
#     return feature_str


# 4. 封装，根据选项以及文件路径生成指纹。默认只调用naive_hash方法
def generate_fingerprint(file_path, methods=None):
    """
    使用指定方法生成文件指纹。

    :param file_path: 文件数据（支持文件路径或字节流）
    :param methods: 指纹生成方法列表，默认且必须有 ["naive_hash"]
    :return: 包含指纹的字典
    """
    if methods is None:
        methods = ["naive_hash"]
    if 'naive_hash' not in methods:
        methods.append('naive_hash')
    fingerprints = {}

    for method in methods:
        try:
            # 返回值：应当包含文件名，文件大小（MB），文件类型（后缀），然后对于每个方法，包含指纹值，指纹方法
            if method == "pHash":
                phash = generate_phash(file_path)
                fingerprints[method] = {
                    "value": phash[0],
                    "method": phash[1]
                }
            elif method == "naive_hash":
                naive_hash = generate_naive_hash(file_path)
                fingerprints[method] = {
                    "value": naive_hash[0],
                    "method": naive_hash[1]
                }
            # elif method == "ai_fingerprint":
            #     fingerprints[method] = {
            #         "value": generate_ai_fingerprint(file_path),
            #         "method": method
            #     }
            else:
                raise ValueError(f"Unknown method: {method}")
            fingerprints["file_name"] = os.path.basename(file_path)
            fingerprints["file_type"] = os.path.splitext(file_path)[1]
            # 小于1M则用KB表示，否则用MB表示
            file_size = os.path.getsize(file_path) / 1024
            if file_size < 1024:
                file_size = f"{file_size:.2f} KB"
            else:
                file_size = f"{file_size/1024:.2f} MB"
            fingerprints["file_size"] = file_size

        except Exception as e:
            fingerprints[method] = {"value": f"Error: {e}", "method": method}

    return fingerprints

# 测试
def generate_fingerprints(file_data):
    """
    使用三种方法生成文件指纹，并输出每个方法的耗时。

    :param file_data: 文件数据（支持文件路径或字节流）
    :return: 包含指纹的字典
    """
    fingerprints = {}

    try:
        start_time = time.time()
        phash = generate_phash(file_data)
        print(f"pHash 耗时: {time.time() - start_time:.4f} 秒")
        fingerprints["phash"] = {
            "value": phash,
            "method": "pHash"
        }
    except Exception as e:
        fingerprints["phash"] = {"value": f"Error: {e}", "method": "pHash"}

    try:
        start_time = time.time()
        naive_hash = generate_naive_hash(file_data)
        print(f"sha256 耗时: {time.time() - start_time:.4f} 秒")
        fingerprints["naive_hash"] = {
            "value": naive_hash,
            "method": "sha256"
        }
    except Exception as e:
        fingerprints["naive_hash"] = {"value": f"Error: {e}", "method": "sha256"}

    # try:
    #     start_time = time.time()
    #     ai_fingerprint = generate_ai_fingerprint(file_data)
    #     print(f"ResNet50 + PCA(16) 耗时: {time.time() - start_time:.4f} 秒")
    #     fingerprints["ai_fingerprint"] = {
    #         "value": ai_fingerprint,
    #         "method": "ResNet50 + Linear(128)"
    #     }
    # except Exception as e:
    #     fingerprints["ai_fingerprint"] = {"value": f"Error: {e}", "method": "ResNet50 + PCA(16)"}
    #     raise e

    """
    耗时比例大约为：
    pHash 耗时: 13.0341 秒
    sha256 耗时: 0.1650 秒
    ResNet50 + PCA(16) 耗时: 16.3674 秒
    """
    return fingerprints



# 示例调用
if __name__ == "__main__":
    file_path = f'{test_path}/image1.jpg'

    # 生成指纹
    fingerprints = generate_fingerprints(file_path)

    # 打印结果
    print(json.dumps(fingerprints, indent=4))
