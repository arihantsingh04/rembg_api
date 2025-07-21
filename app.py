from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io
import requests
import os

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    image = None

    if 'image' in request.files and request.files['image'].filename != '':
        image = Image.open(request.files['image'].stream).convert("RGBA")
    elif 'image_url' in request.form:
        try:
            resp = requests.get(request.form['image_url'])
            image = Image.open(io.BytesIO(resp.content)).convert("RGBA")
        except Exception:
            return jsonify({'error': 'Failed to load image from URL'}), 400
    else:
        return jsonify({'error': 'No image provided'}), 400

    output = remove(image)
    img_io = io.BytesIO()
    output.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
