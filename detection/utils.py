# detection/utils.py
import numpy as np
from tensorflow.keras.preprocessing import image   # pyright: ignore[reportMissingImports]
from tensorflow.keras.models import load_model # pyright: ignore[reportMissingImports]
from django.conf import settings
import os

MODEL_PATH = os.path.join(settings.BASE_DIR, "models", "cnn_model.keras")
model = load_model(MODEL_PATH)

CLASS_NAMES = ["alopecia", "dandruff", "normal"]

def predict_hair_condition(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)[0]

    confidence = float(np.max(predictions))
    predicted_class = CLASS_NAMES[np.argmax(predictions)]

    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
    }
