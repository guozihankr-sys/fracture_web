from flask import Flask, request, render_template_string
from model import predict

app = Flask(__name__)

HTML = """
<h2>🦴 AI骨折检测系统</h2>

<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="上传并分析">
</form>

{% if result %}
<hr>
<h3>{{ result }}</h3>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def upload():
    result = None

    if request.method == "POST":
        file = request.files["file"]

        if file:
            # 保存图片
            filepath = "temp.jpg"
            file.save(filepath)

            # AI预测
            prob = predict(filepath)

            if prob > 0.5:
                result = f"⚠️ 疑似骨折（概率：{prob:.2f}）"
            else:
                result = f"✅ 未检测到明显骨折（概率：{1-prob:.2f}）"

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
