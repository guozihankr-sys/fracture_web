from PIL import Image
import numpy as np

def predict(img_path):
    image = Image.open(img_path).convert("L")
    img = np.array(image)

    # 基础特征
    contrast = img.std()          # 对比度
    brightness = img.mean()       # 亮度

    # 边缘检测（关键！）
    edge = np.abs(np.diff(img, axis=0)).mean() + np.abs(np.diff(img, axis=1)).mean()

    # 综合评分（更稳）
    score = (
        (contrast / 60) * 0.4 +     # 对比度权重
        (edge / 20) * 0.5 +         # 边缘（骨折关键）
        (brightness / 255) * 0.1    # 亮度辅助
    )

    prob = round(min(score, 1.0), 2)

    # 更合理阈值
    if prob > 0.55:
        return "检测到骨折", prob
    else:
        return "未检测到骨折", prob
