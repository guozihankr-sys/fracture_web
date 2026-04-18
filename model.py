from PIL import Image
import numpy as np
import cv2

def predict(img_path):
    # 读取图片
    image = Image.open(img_path).convert("L")
    img = np.array(image)

    # 边缘检测
    edges = cv2.Canny(img, 50, 150)
    edge_count = np.sum(edges > 0)

    # 亮度
    brightness = np.mean(img)

    # 简单规则（比随机聪明很多）
    score = edge_count / 10000 + brightness / 255

    prob = round(min(score, 1.0), 2)

    if prob > 0.5:
        return "检测到骨折", prob
    else:
        return "未检测到骨折", prob
