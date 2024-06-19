from config import *

def triangulate(kp1, kp2, P1, P2):
    # 创建一个 4x4 的矩阵 A
    A = np.zeros((4, 4), dtype=np.float32)

    # 填充矩阵 A
    A[0] = kp1.pt[0] * P1[2] - P1[0]
    A[1] = kp1.pt[1] * P1[2] - P1[1]
    A[2] = kp2.pt[0] * P2[2] - P2[0]
    A[3] = kp2.pt[1] * P2[2] - P2[1]

    # 进行 SVD 分解
    _, _, vt = cv2.SVDecomp(A)

    # 提取 3D 点
    x3D = vt[-1].reshape(-1)

    # 归一化 3D 点
    x3D = x3D[:3] / x3D[3]

    return x3D

# 三角化恢复 3D 点
def restore(kp, P):
    kp_1, kp_2, kp_3, kp_4 = kp
    P1, P2, P3, P4 = P
    x3D_1 = triangulate(kp_1, kp_2, P1, P2)
    x3D_2 = triangulate(kp_1, kp_3, P1, P3)
    x3D_3 = triangulate(kp_1, kp_4, P1, P4)
    x3D_4 = triangulate(kp_2, kp_3, P2, P3)
    x3D_5 = triangulate(kp_2, kp_4, P2, P4)
    x3D_6 = triangulate(kp_3, kp_4, P3, P4)
    # print(x3D_1)
    # print(x3D_2)
    # print(x3D_3)
    # print(x3D_4)
    # print(x3D_5)
    # print(x3D_6)
    average_point1 = (x3D_1 + x3D_2 + x3D_3 + x3D_4 + x3D_5 + x3D_6) / 6.0
    X = np.append(average_point1, 1.0)
    return X

X_1 = restore(kp1, P)
X_2 = restore(kp2, P)
X_3 = restore(kp3, P)
X_4 = restore(kp4, P)
print(X_1)  #B
print(X_2)  #A
print(X_3)  #C
print(X_4)  #D

x3D_5 = triangulate(kp5_3, kp5_4, P3, P4)
X_5 = np.append(x3D_5, 1.0)
print(X_5)  #G

x3D_6 = triangulate(kp6_3, kp6_4, P3, P4)
X_6 = np.append(x3D_6, 1.0)
print(X_6)  #M

x3D_7 = triangulate(kp7_3, kp7_4, P3, P4)
X_7 = np.append(x3D_7, 1.0)
print(X_7)  #N


def erwei(X):
    P = K2 @ RT2 @ X
    P = P / P[2]
    P = np.floor(P)
    P = P[:-1]
    P_int = P.astype(int)
    return P_int

A = erwei(X_2)
B = erwei(X_1)
C = erwei(X_3)
D = erwei(X_4)

# 定义图像大小
width, height = 1280, 960

# 创建一个白色背景的图像
image = np.ones((height, width, 3), dtype=np.uint8) * 255

# 将四个点的坐标放入 NumPy 数组
points = np.array([A, B, C, D], dtype=np.int32)
points = points.reshape((-1, 1, 2))

# 绘制黑色的点
for point in [A, B, C, D]:
    cv2.circle(image, point, radius=5, color=(0, 0, 0), thickness=-1)

# 绘制连接四个点的红色线，形成四边形
cv2.line(image, A, B, color=(0, 0, 255), thickness=2)
cv2.line(image, B, C, color=(0, 0, 255), thickness=2)
cv2.line(image, C, D, color=(0, 0, 255), thickness=2)
cv2.line(image, D, A, color=(0, 0, 255), thickness=2)

# 填充四边形的中间区域为灰色
cv2.fillPoly(image, [points], color=(128, 128, 128))

# 显示图像
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存图像
cv2.imwrite('./data/quadrilateral.png', image)