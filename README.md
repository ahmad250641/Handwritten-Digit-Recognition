Handwritten Digit Recognition Web Application

A complete web application that allows users to draw a digit (0-9) on an HTML canvas and uses a Convolutional Neural Network (CNN) to predict the drawn digit in real-time.

This project is developed as part of the Machine Learning course assignment.

👥 Team Members

This project was collaboratively developed by:

Ahmad (ID: 250641) - ML Model Engineering

Raneem (ID: 322697) - Image Preprocessing Logic

Ahmad (ID: 327860) - Flask API & Backend

Raneem (ID: 327640) - Frontend UI/UX (HTML/CSS)

Mawadah (ID: 280627) - Canvas JS Integration & Deployment

🚀 Features

Interactive Canvas: Draw digits smoothly using mouse or touch.

Smart Preprocessing: Advanced image processing that handles transparent backgrounds, centers the digit, and scales it to match the exact format of the MNIST dataset.

Real-time Prediction: Fast inference returning the predicted digit along with the top 3 confidence percentages.

🛠️ Tech Stack

Machine Learning: Python, TensorFlow, Keras, NumPy

Backend API: Flask, Pillow (PIL)

Frontend: HTML5, CSS3, Vanilla JavaScript

🧠 Model & Image Preprocessing

The core of this application is a CNN trained on the MNIST dataset. Since a web canvas produces an RGBA image that differs significantly from MNIST images, we implemented a robust preprocessing pipeline:

Replaces the transparent canvas background with a solid white background.

Converts the image to grayscale and inverts colors (white digit on a black background).

Applies a threshold to remove noise.

Calculates the bounding box of the drawn digit to crop empty spaces.

Resizes the cropped digit to 20x20 pixels using Lanczos resampling.

Centers the digit on a 28x28 black canvas.

Normalizes pixel values to [0, 1] before feeding them to the CNN.

💻 How to Run Locally

1. Clone the repository

git clone [https://github.com/ahmad250641/Handwritten-Digit-Recognition.git](https://github.com/ahmad250641/Handwritten-Digit-Recognition.git)
cd Handwritten-Digit-Recognition


2. Install dependencies

Make sure you have Python installed, then run:

pip install -r requirements.txt


3. Train the Model

Before starting the server, you need to generate the .keras model file:

python train_model.py


(This will download the MNIST dataset, train the CNN, and save the model inside the model/ folder).

4. Run the Flask Server

python app.py


5. Open the App

Open your web browser and navigate to:
http://127.0.0.1:5000/

Deployed Application URL:  https://huggingface.co/spaces/Mawadah280627/Handwritten-Digit-Recognition