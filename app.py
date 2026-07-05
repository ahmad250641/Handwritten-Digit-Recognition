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

