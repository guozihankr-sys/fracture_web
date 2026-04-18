from PIL import Image
import numpy as np

def predict(img_path):
    image = Image.open(img_path).convert("L")
    img = np.array(image).astype(float)

    # 梯度（找断裂）
    gx = np.abs(np.diff(img, axis=1))
    gy = np.abs(np.diff(img, axis=0))
    grad = (gx.mean() + gy.mean()) / 2

    # 对比度
    contrast = img.std()

    # 👉 核心：检测“异常突变”（骨折更明显）
    threshold = img.mean() + 1.5 * img.std()
    abnormal = (img > threshold).mean()

    # 👉 简单稳定评分（不要复杂）
    score = 0.5 * (grad / 40) + 0.4 * abnormal + 0.1 * (contrast / 80)

    prob = round(min(score, 1.0), 2)

    if prob > 0.5:
        return "检测到骨折", prob
    else:
        return "未检测到骨折", prob
