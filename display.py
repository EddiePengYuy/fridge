import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import matplotlib.animation as animation
from feature_points import XY_coords

# 立方体的顶点坐标
A = np.array([-0.28490049, -0.76271677, 1.89456999])
B = np.array([-0.26498026, 0.36477622, 2.72778583])
C = np.array([0.14090927, 0.09310543, 3.07460856])
D = np.array([0.12223041, -1.02159131, 2.23594666])
M = np.array([0.17056599, 0.34357563, 3.25435519])
N = np.array([-0.3063356, 0.09691617, 3.63260484])
MN = N - M
E = A + MN
F = B + MN
G = C + MN
H = D + MN

# 立方体的面
faces = [
    ['A', 'B', 'C', 'D'],  # 正面
    ['E', 'F', 'G', 'H'],  # 背面
    ['A', 'B', 'F', 'E'],  # 底面
    ['B', 'C', 'G', 'F'],  # 右面
    ['C', 'D', 'H', 'G'],  # 顶面
    ['D', 'A', 'E', 'H'],  # 左面
    ['X', 'Y', 'C', 'D']   # 门
]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def update(num, XY_coords, faces, ax):
    ax.cla()
    points = {
        'A': A,
        'B': B,
        'C': C,
        'D': D,
        'E': E,
        'F': F,
        'G': G,
        'H': H,
        'X': XY_coords[num][0],
        'Y': XY_coords[num][1]
    }
    # 绘制立方体的顶点
    for point, coord in points.items():
        ax.scatter(*coord, color='b')
        ax.text(*coord, '%s' % point, size=20, zorder=1, color='k')

    # 绘制立方体的面，设置不同颜色
    for face in faces:
        verts = [points[vertex] for vertex in face]
        if face == ['X', 'Y', 'C', 'D']:
            color = 'grey'
        else:
            color = 'blue'
        ax.add_collection3d(Poly3DCollection([verts], facecolors=color, linewidths=1, edgecolors='r', alpha=.5))

    # 设置视角，使ABCD面正对我们
    ax.view_init(elev=-90, azim=-90)
    # 设置固定的轴范围
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1.5, 0.5)
    ax.set_zlim3d(1, 4)
    # 删除网格线
    ax.grid(False)
    # 隐藏坐标轴
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

ani = animation.FuncAnimation(fig, update, frames=len(XY_coords), fargs=(XY_coords, faces, ax), interval=125, repeat=False)

# 保存动画到文件
ani.save('animation.gif', writer='pillow', fps=8)

plt.show()
