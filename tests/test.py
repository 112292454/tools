import numpy as np


def compute_normalized_laplacian(A):
    # 计算度矩阵 D
    D = np.diag(np.sum(A, axis=1))  # 行求和，得到度矩阵 D

    # 计算拉普拉斯矩阵 L
    L = D - A

    # 计算对称正则化拉普拉斯矩阵: D^(-1/2) L D^(-1/2)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(np.diagonal(D)))  # D^(-1/2)

    # 计算正则化后的拉普拉斯矩阵
    L_normalized = D_inv_sqrt @ L @ D_inv_sqrt

    # 返回正则化后的拉普拉斯矩阵并四舍五入到两位小数
    return np.round(L_normalized, 2)


# 示例邻接矩阵
A = np.array([[0, 1,0,0, 1, 0],
              [1,0,1,0,1,0],
              [0, 1, 0, 1, 0, 0],
              [0, 0, 1, 0, 1, 1],
              [1, 1, 0, 1, 0, 0],
              [0, 0, 0, 1, 0, 0],])
              # 计算正则化后的拉普拉斯矩阵
L_normalized = compute_normalized_laplacian(A)

print("Normalized Laplacian Matrix:")
print(L_normalized)
