from flask import Flask, render_template, request
import os
from model import predict

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    prob = None
    img_path = None

    if request.method == 'POST':
        file = request.files.get('file')

        if file and file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            result, prob = predict(filepath)

            # ⭐ 关键修复（必须有 /）
            img_path = '/' + filepath

    return render_template('index.html',
                           result=result,
                           prob=prob,
                           img_path=img_path)

if __name__ == '__main__':
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
