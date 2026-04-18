from PIL import Image
import numpy as np

def predict(img_path):
    image = Image.open(img_path).convert("L")
    img = np.array(image)

    contrast = img.std()
    brightness = img.mean()

    score = 0.6 * (contrast / 80) + 0.4 * (brightness / 255)
    prob = round(min(score, 1.0), 2)

    if prob > 0.55:
        return "检测到骨折", prob
    else:
        return "未检测到骨折", prob
