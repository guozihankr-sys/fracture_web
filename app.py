from flask import Flask, render_template, request
import os
from model import predict

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "没有文件"

        file = request.files['file']

        if file.filename == '':
            return "文件为空"

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            result, prob = predict(filepath)
        except Exception as e:
            return f"模型报错：{str(e)}"

        return f"""
        <h2>{result}（概率: {prob}）</h2>
        <img src='/{filepath}' width='300'>
        <br><br>
        <a href="/">返回</a>
        """

    return """
    <h2>AI骨折检测系统（修复版）</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">上传</button>
    </form>
    """
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
