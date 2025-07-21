
from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
import os


app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return {'error': 'No image uploaded'}, 400

    image_file = request.files['image']
    input_image = Image.open(image_file.stream).convert("RGBA")
    output_image = remove(input_image)

    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
