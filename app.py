from flask import Flask, request, render_template_string
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import base64
from io import BytesIO

app = Flask(__name__)

# =========================
# 🧠 1. 加载预训练模型（ResNet）
# =========================

model = models.resnet18(pretrained=True)

# 改最后一层 → 二分类
model.fc = torch.nn.Linear(model.fc.in_features, 1)

model.eval()

# =========================
# 🧠 2. 图像预处理
# =========================

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# =========================
# 🎨 页面
# =========================

HTML = """
<h2>🧠 AI骨折检测系统（真实模型版）</h2>

<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="上传并分析">
</form>

{% if result %}
<hr>
<h3>分析结果：</h3>
<p>{{ result }}</p>
<img src="{{ image_url }}" width="300">
{% endif %}
"""

# =========================
# 🚀 主逻辑
# =========================

@app.route("/", methods=["GET", "POST"])
def upload():
    result = None
    image_url = None

    if request.method == "POST":
        file = request.files["file"]

        if file:
            image = Image.open(file).convert("RGB")

            img_tensor = transform(image).unsqueeze(0)

            with torch.no_grad():
                output = model(img_tensor)
                prob = torch.sigmoid(output).item()

            if prob > 0.5:
                result = f"⚠️ 疑似骨折（概率：{prob:.2f}）"
            else:
                result = f"✅ 正常（概率：{1-prob:.2f}）"

            # 显示图片
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            image_url = "data:image/png;base64," + img_str

    return render_template_string(HTML, result=result, image_url=image_url)

if __name__ == "__main__":
    app.run()
