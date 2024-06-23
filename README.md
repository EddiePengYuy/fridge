# fridge
# 项目介绍
本项目通过多视图几何及LK光流法实现了冰箱顶点的三维坐标恢复及冰箱门3D打开角度的估计。

# 环境依赖
- Python 3.12
- numpy
- matplotlib
- opencv-python

# 目录结构描述
├── config.py          // 保存相机参数及冰箱顶点像素坐标  
├── LK光流法.py       // LK光流法追踪冰箱门上边缘特征点  
├── feature_points.py  // 重建特征点三维坐标  
├── display.py         // 三维可视化  
├── vertices.py        // 三角化恢复3D坐标  
├── data               // 输入数据  
    链接：https://pan.baidu.com/s/1BF5wPHyUDbjlejOul-Id1w?pwd=3cpy 
    提取码：3cpy
│   ├── 1.avi          // 第一视角视频  
│   ├── 2.avi          // 第二视角视频  
│   ├── 3.avi          // 第三视角视频  
│   ├── 4.avi          // 第四视角视频  
│   └── calibration.avi // 640*480像素图像相机相对参数  
└── output             // 输出结果  
│   ├── animation.gif      // 三维可视化GIF格式输出  
│   ├── tracked_video.avi  // 特征点追踪结果  
│   ├── tracked_points.txt // 特征点二维像素坐标  
│   └── demo.mp4           // 对比结果  
