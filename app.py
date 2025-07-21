from flask import Flask, request, render_template_string, send_file
from rembg import remove
from PIL import Image
import io
import requests
import os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Background Remover</title>
    <style>
        body { font-family: Arial, sans-serif; background: #111; color: #eee; text-align: center; padding: 40px; }
        input[type="file"], input[type="text"] { margin: 10px; padding: 10px; border-radius: 5px; }
        button { padding: 10px 20px; background: #007bff; border: none; color: white; border-radius: 5px; cursor: pointer; }
        img { margin-top: 20px; max-width: 300px; border-radius: 10px; }
        .container { background: #222; padding: 30px; border-radius: 15px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Background Remover</h1>
        <form method="POST" enctype="multipart/form-data">
            <div>
                <label>Upload Image:</label><br>
                <input type="file" name="image">
            </div>
            <div>
                <label>Or enter image URL:</label><br>
                <input type="text" name="image_url" placeholder="https://example.com/image.png">
            </div>
            <button type="submit">Remove Background</button>
        </form>

        {% if result %}
            <h2>Result:</h2>
            <img src="{{ url_for('output') }}" alt="Output Image">
        {% endif %}
    </div>
</body>
</html>
'''

output_image_bytes = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global output_image_bytes
    result = False
    if request.method == 'POST':
        image = None

        if 'image' in request.files and request.files['image'].filename != '':
            image = Image.open(request.files['image'].stream).convert("RGBA")
        elif request.form.get('image_url'):
            try:
                resp = requests.get(request.form.get('image_url'))
                image = Image.open(io.BytesIO(resp.content)).convert("RGBA")
            except Exception:
                return "Failed to load image from URL", 400

        if image:
            output = remove(image)
            img_io = io.BytesIO()
            output.save(img_io, 'PNG')
            img_io.seek(0)
            output_image_bytes = img_io.read()
            result = True

    return render_template_string(HTML, result=result)

@app.route('/output')
def output():
    global output_image_bytes
    if output_image_bytes:
        return send_file(io.BytesIO(output_image_bytes), mimetype='image/png')
    return "No image processed", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
