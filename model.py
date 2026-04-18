from PIL import Image
import numpy as np

def predict(img_path):
    image = Image.open(img_path).convert("L")
    img = np.array(image)

    # 对比度
    contrast = img.std()

    # 亮度
    brightness = img.mean()

    # ⭐ 重新设计评分（更合理）
    contrast_score = contrast / 80      # 控制范围
    brightness_score = brightness / 255

    # 加权（重点）
    score = 0.6 * contrast_score + 0.4 * brightness_score

    prob = round(min(score, 1.0), 2)

    if prob > 0.55:
        return "检测到骨折", prob
    else:
        return "未检测到骨折", prob
