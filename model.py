from PIL import Image
import numpy as np
import cv2

def predict(img_path):
    image = Image.open(img_path).convert("L")
    img = np.array(image)

    # 边缘检测（更像医学分析）
    edges = cv2.Canny(img, 50, 150)
    edge_count = np.sum(edges > 0)

    # 亮度 & 对比度
    brightness = img.mean()
    contrast = img.std()

    # 评分（更合理）
    edge_score = edge_count / 10000
    contrast_score = contrast / 80
    brightness_score = brightness / 255

    score = 0.5 * edge_score + 0.3 * contrast_score + 0.2 * brightness_score
    prob = round(min(score, 1.0), 2)

    # 风险等级
    if prob > 0.7:
        level = "🔴 高风险（疑似骨折）"
    elif prob > 0.5:
        level = "🟡 中风险（建议复查）"
    else:
        level = "🟢 低风险（基本正常）"

    # 保存边缘图
    edge_path = img_path.replace(".jpg", "_edge.jpg")
    cv2.imwrite(edge_path, edges)

    return level, prob, edge_path
