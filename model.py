import random

def predict(img_path):
    prob = round(random.uniform(0, 1), 2)  # 改这里

    if prob > 0.5:
        return "检测到骨折", prob
    else:
        return "未检测到骨折", prob
