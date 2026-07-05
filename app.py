import os
import re
import io
import base64
import numpy as np

from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps

app = Flask(__name__)

# ==========================
# Load Trained Model
# ==========================

MODEL_PATH = "model/digit_model.keras"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "Model not found! Please run train_model.py first."
    )

model = load_model(MODEL_PATH)


# ==========================
# Image Preprocessing
# ==========================

def preprocess_image(image):
    """
    Convert the canvas image into an MNIST-like image.
    """

    # Convert to grayscale
    image = image.convert("L")

    # Invert colors (white digit on black background)
    image = ImageOps.invert(image)

    # Convert to numpy
    img = np.array(image)

    # Remove background noise
    img[img < 30] = 0

    # Detect digit boundaries
    coords = np.argwhere(img > 0)

    # Empty canvas
    if coords.size == 0:
        return np.zeros((1, 28, 28, 1), dtype=np.float32)

    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1

    # Crop digit
    img = img[y0:y1, x0:x1]

    image = Image.fromarray(img)

    # Keep aspect ratio
    image.thumbnail((20, 20), Image.Resampling.LANCZOS)

    # Create black background
    background = Image.new("L", (28, 28), 0)

    # Center the digit
    offset_x = (28 - image.size[0]) // 2
    offset_y = (28 - image.size[1]) // 2

    background.paste(image, (offset_x, offset_y))

    # Normalize
    img = np.array(background).astype("float32") / 255.0

    # CNN input shape
    img = img.reshape(1, 28, 28, 1)

    return img


# ==========================
# Routes
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        if not data or "image" not in data:
            return jsonify({
                "error": "No image received."
            }), 400

        image_data = data["image"]

        match = re.search(r"base64,(.*)", image_data)

        if not match:
            return jsonify({
                "error": "Invalid image format."
            }), 400

        image_bytes = base64.b64decode(match.group(1))

        image = Image.open(io.BytesIO(image_bytes))

        processed_image = preprocess_image(image)

        prediction = model.predict(processed_image, verbose=0)[0]

        digit = int(np.argmax(prediction))

        confidence = float(np.max(prediction) * 100)

        # Top 3 predictions
        top3_idx = prediction.argsort()[-3:][::-1]

        top3 = []

        for i in top3_idx:
            top3.append({
                "digit": int(i),
                "confidence": round(float(prediction[i] * 100), 2)
            })

        return jsonify({

            "digit": digit,

            "confidence": round(confidence, 2),

            "top3": top3

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# ==========================
# Run Application
# ==========================

if __name__ == "__main__":
    app.run(debug=True)