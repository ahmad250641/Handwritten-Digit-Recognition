import os
import numpy as np

from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout
)
from tensorflow.keras.utils import to_categorical

# إنشاء مجلد النموذج
os.makedirs("model", exist_ok=True)

# تحميل البيانات
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# تطبيع البيانات
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# إضافة بعد القناة (Channel)
x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

# One-Hot Encoding
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# بناء نموذج CNN
model = Sequential([

    Conv2D(
        32,
        (3,3),
        activation="relu",
        input_shape=(28,28,1)
    ),

    MaxPooling2D((2,2)),

    Conv2D(
        64,
        (3,3),
        activation="relu"
    ),

    MaxPooling2D((2,2)),

    Flatten(),

    Dense(
        128,
        activation="relu"
    ),

    Dropout(0.5),

    Dense(
        10,
        activation="softmax"
    )

])

# تجميع النموذج
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

print("Training...")

history = model.fit(
    x_train,
    y_train,
    epochs=10,
    batch_size=64,
    validation_split=0.1,
    verbose=1
)

loss, accuracy = model.evaluate(
    x_test,
    y_test,
    verbose=0
)

print(f"\nAccuracy = {accuracy*100:.2f}%")
print(f"Loss = {loss:.4f}")

model.save("model/digit_model.keras")

print("\nModel saved successfully.")