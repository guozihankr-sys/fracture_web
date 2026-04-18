from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<h2>🦴 骨折影像分析（基础版）</h2>

<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="上传并分析">
</form>

{% if result %}
<h3>{{ result }}</h3>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def upload():
    result = None

    if request.method == "POST":
        file = request.files["file"]
        if file:
            result = "✅ 图片上传成功（网站已恢复）"

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run()
