import numpy as np
import matplotlib.pyplot as plt
from config import P4

d = np.array([774, 26])
# 定义三个点的坐标
A = np.array([-0.28490049, -0.76271677, 1.89456999])
C = np.array([0.14090927, 0.09310543, 3.07460856])
D = np.array([0.12223041, -1.02159131, 2.23594666])
# G = np.array([-0.34516039, -0.08474126, 3.4916966])
M = np.array([0.17056599, 0.34357563, 3.25435519])
N = np.array([-0.3063356, 0.09691617, 3.63260484])
MN = N - M
# CG = G - C
H = D + MN

AD = D - A
AH = H - A
DC = C - D
# 计算法向量（单位向量）
normal = np.cross(AD, AH)
normal = normal / np.linalg.norm(normal)

# 半径
radius = np.linalg.norm(AD)

# 生成半圆上的点并存入F
angles = np.deg2rad(np.arange(180, 360, 1))  # 1度间隔
F = np.array([D + radius * (np.cos(angle) * AD / np.linalg.norm(AD) + np.sin(angle) * np.cross(normal, AD) / np.linalg.norm(np.cross(normal, AD))) for angle in angles])

# # 创建一个三维图形对象
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# # 绘制点集F
# ax.scatter(F[:, 0], F[:, 1], F[:, 2], c='r', marker='o', label='F points')
#
# # 绘制A, D, H点
# ax.scatter([A[0], D[0], H[0]], [A[1], D[1], H[1]], [A[2], D[2], H[2]], c='b', marker='^', label='ADH points')
#
# # 标记A, D, H点的名称
# ax.text(A[0], A[1], A[2], 'A', color='black')
# ax.text(D[0], D[1], D[2], 'D', color='black')
# ax.text(H[0], H[1], H[2], 'H', color='black')
#
# # 计算ADH平面的法向量
# normal = np.cross(D - A, H - A)
# d = -A.dot(normal)
#
# # 创建网格以绘制平面
# xx, yy = np.meshgrid(np.linspace(-1, 1, 10), np.linspace(-2, 1, 10))
# zz = (-normal[0] * xx - normal[1] * yy - d) / normal[2]
#
# # 绘制平面
# ax.plot_surface(xx, yy, zz, alpha=0.5, color='gray')
#
# # 设置坐标轴标签
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
#
#
# # 设置图例
# ax.legend()
#
# # 显示图形
# plt.show()

F_prime = []
# 已有相机的内参矩阵 K4 和外参矩阵 RT4
for f in F:
    f_prime = np.append(f, 1)
    F_temp = P4 @ f_prime
    result = np.floor_divide(F_temp, F_temp[2])
    F_prime.append(result[:-1])

F_prime = np.array(F_prime)
# 创建一个1280x960的画布
plt.figure(figsize=(12.8, 9.6))  # figsize 参数的单位是英寸，1280 像素 / 100 dpi = 12.8 英寸，960 像素 / 100 dpi = 9.6 英寸

# 绘制点集，使用红色
plt.scatter(F_prime[:, 0], F_prime[:, 1], c='red')

# 设置坐标轴范围以确保所有点都在画布内
plt.xlim(0, 1280)
plt.ylim(960, 0)

# 显示网格以便更容易查看点的位置
plt.grid(True)

# 显示图形
plt.show()

# 存储直线方程的列表
lines = []

for point in F_prime:
    x1, y1 = point
    x2, y2 = d

    # 计算斜率m
    if x2 - x1 != 0:
        m = (y2 - y1) / (x2 - x1)
    else:
        m = float('inf')  # 垂直线的斜率为无穷大

    # 计算截距b
    if m != float('inf'):
        b = y1 - m * x1
    else:
        b = x1  # 对于垂直线，截距用x表示

    # 将直线方程存储到列表中
    lines.append((m, b))

# 读取文件
file_path = './data/tracked_points.txt'
# 加载数据
data = np.loadtxt(file_path, delimiter=' ')

# 存储每个点到最短距离直线的下标
min_distance_indices = []

for point in data:
    x0, y0 = point
    min_distance = float('inf')
    min_index = -1

    for i, (m, b) in enumerate(lines):
        if m == float('inf'):
            distance = abs(x0 - b)
        else:
            distance = abs(m * x0 - y0 + b) / np.sqrt(m ** 2 + 1)

        if distance < min_distance:
            min_distance = distance
            min_index = i

    min_distance_indices.append(min_index)

# 按下标集和从点集F中取出对应的点
selected_points = F[min_distance_indices]
Y = selected_points + DC

# 合并点集为所需的XY_coords格式
XY_coords = [(selected_points[i], Y[i]) for i in range(len(selected_points))]

# # 示例输出
# for coord in XY_coords:
#     print(coord)
# print(len(XY_coords))