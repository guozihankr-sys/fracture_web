from PIL import Image, ImageFilter
import numpy as np

def predict(img_path):
    # 读图（灰度）
    image = Image.open(img_path).convert("L")
    img = np.array(image).astype(np.float32)

    # 1) 基础特征
    contrast = img.std()           # 对比度
    brightness = img.mean()        # 亮度

    # 2) 梯度（边缘强度）
    gx = np.abs(np.diff(img, axis=1))
    gy = np.abs(np.diff(img, axis=0))
    grad = (gx.mean() + gy.mean()) / 2.0

    # 3) “异常边缘比例”（关键升级）
    #    用边缘滤波 + 阈值，统计特别“突兀”的边缘占比（更像断裂线）
    edges = image.filter(ImageFilter.FIND_EDGES)
    e = np.array(edges).astype(np.float32)
    thr = e.mean() + 1.2 * e.std()         # 自适应阈值
    abnormal_ratio = (e > thr).mean()      # 异常边缘占比（0~1）

    # 4) 归一化 & 加权（权重偏向“异常边缘”）
    contrast_s = contrast / 80.0
    brightness_s = brightness / 255.0
    grad_s = grad / 40.0

    score = (
        0.45 * abnormal_ratio +   # 关键：断裂感
        0.30 * grad_s +           # 边缘强度
        0.20 * contrast_s +       # 结构复杂度
        0.05 * brightness_s       # 辅助
    )

    prob = round(float(min(score, 1.0)), 2)

    # 阈值略提高，减少“全判骨折”
    if prob > 0.6:
        return "检测到骨折", prob
    else:
        return "未检测到骨折", prob
