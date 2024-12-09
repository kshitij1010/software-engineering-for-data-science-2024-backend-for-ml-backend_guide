from flask import Blueprint, request, jsonify
from ultralytics import YOLO
import io
from PIL import Image

classifier_service = Blueprint("classifier", __name__)

# Load YOLO model
model = YOLO("yolo11n-cls.pt")

@classifier_service.route("/classify", methods=["POST"])
def classify():
    try:
        file = request.files["image"]
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        results = model.predict(img)
        formatted_results = [
            {"class": result.names[int(pred[0])], "confidence": float(pred[1])}
            for pred in results[0].probs.tolist()
        ]

        return jsonify({"results": formatted_results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500