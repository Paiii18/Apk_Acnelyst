import numpy as np
import tensorflow as tf
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
from . import api_bp
from ...extensions import db
from ...models.prediction import Prediction
from flask_login import current_user
from flask import url_for

# Load model saat pertama kali
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "model", "AcneModel.tflite")
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Info tensor
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Konfigurasi upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Tidak ada file yang diupload"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Nama file kosong"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Preprocessing gambar
        img = tf.keras.utils.load_img(filepath, target_size=(224, 224))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Jalankan inferensi
        interpreter.set_tensor(input_details[0]["index"], img_array.astype(np.float32))
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]["index"])
        prediction = output_data.tolist()

        # Contoh mapping label
        labels = ["acne", "normal"]
        predicted_index = int(np.argmax(prediction))
        result_label = labels[predicted_index]
        confidence = float(np.max(prediction))

        return jsonify({
            "label": result_label,
            "confidence": confidence
        })
    
    user_id = current_user.id if getattr(current_user, "is_authenticated", False) else None

    pred = Prediction(
        user_id=user_id,
        filename=filename,
        label=label,
        confidence=conf,
    )
    db.session.add(pred)
    db.session.commit()

    # balikan juga id & url file (biar Flutter gampang)
    file_url = url_for("main.uploaded_file", filename=filename, _external=True)
    return jsonify({"id": pred.id, "label": label, "confidence": conf, "image_url": file_url})

    return jsonify({"error": "Format file tidak diizinkan"}), 400
