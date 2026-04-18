import random

def predict(img_path):
    prob = round(random.uniform(0.3, 0.9), 2)

    if prob > 0.5:
        return "fracture", prob
    else:
        return "normal", prob
