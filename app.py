from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<h2>骨折影像分析（第一版）</h2>

<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="上传并分析">
</form>

{% if result %}
<p>分析结果：{{ result }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def upload():
    result = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            result = "已成功上传图片（下一步做AI分析）"
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run()
