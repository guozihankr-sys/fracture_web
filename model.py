from PIL import Image, ImageFilter
import numpy as np

def predict(img_path):
    image = Image.open(img_path).convert("L")

    # 原始图
    img = np.array(image)

    # 边缘检测（关键升级）
    edges = image.filter(ImageFilter.FIND_EDGES)
    edge_array = np.array(edges)

    # 特征
    contrast = img.std()              # 对比度
    brightness = img.mean()          # 亮度
    edge_strength = edge_array.mean()  # 边缘强度（新增）

    # 更“聪明”的评分
    score = (
        0.4 * (contrast / 80) +
        0.3 * (brightness / 255) +
        0.3 * (edge_strength / 50)
    )

    prob = round(min(score, 1.0), 2)

    if prob > 0.6:
        return "检测到骨折", prob
    else:
        return "未检测到骨折", prob
