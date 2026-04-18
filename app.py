from flask import Flask, request, render_template_string
from PIL import Image
import numpy as np
import cv2
import base64
from io import BytesIO

app = Flask(__name__)

HTML = """
<h2>🦴 骨折影像分析系统（升级版）</h2>

<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="上传并分析">
</form>

{% if result %}
<hr>
<p><b>分析结果：</b>{{ result }}</p>

<h3>原始图像：</h3>
<img src="data:image/png;base64,{{ original_img }}" width="300">

<h3>边缘检测图：</h3>
<img src="data:image/png;base64,{{ edge_img }}" width="300">
{% endif %}
"""

def image_to_base64(img):
    buffer = BytesIO()
    Image.fromarray(img).save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

@app.route("/", methods=["GET", "POST"])
def upload():
    result = None
    original_img = None
    edge_img = None

    if request.method == "POST":
        file = request.files["file"]

        if file:
            image = Image.open(file).convert("L")
            img = np.array(image)

            edges = cv2.Canny(img, 50, 150)
            edge_count = np.sum(edges > 0)

            if edge_count > 5000:
                result = "⚠️ 可能存在骨折（边缘异常较多）"
            else:
                result = "✅ 未检测到明显骨折"

            # 转 base64 显示
            original_img = image_to_base64(img)
            edge_img = image_to_base64(edges)

    return render_template_string(
        HTML,
        result=result,
        original_img=original_img,
        edge_img=edge_img
    )

if __name__ == "__main__":
    app.run()
