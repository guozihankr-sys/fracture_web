from flask import Flask, request, render_template_string
from PIL import Image
import numpy as np
import cv2
import torch
import torchvision.transforms as transforms

app = Flask(__name__)

# 👉 模拟AI模型（用随机值代替真实预测）
def fake_ai_predict(img):
    return np.random.rand()  # 返回0~1概率

# 👉 图像预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

HTML = """
<h2>🧠 AI骨折检测系统（升级版）</h2>

<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="上传并分析">
</form>

{% if result %}
<h3>分析结果：</h3>
<p>{{ result }}</p>
<img src="{{ image_url }}" width="300">
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def upload():
    result = None
    image_url = None

    if request.method == "POST":
        file = request.files["file"]

        if file:
            image = Image.open(file).convert("RGB")

            # 👉 AI输入
            img_tensor = transform(image).unsqueeze(0)

            # 👉 AI预测（现在是假的）
            prob = fake_ai_predict(img_tensor)

            if prob > 0.5:
                result = f"⚠️ 疑似骨折（概率：{prob:.2f}）"
            else:
                result = f"✅ 正常（概率：{1-prob:.2f}）"

            # 👉 转base64显示图片
            import base64
            from io import BytesIO
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            image_url = "data:image/png;base64," + img_str

    return render_template_string(HTML, result=result, image_url=image_url)

if __name__ == "__main__":
    app.run()
