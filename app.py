from flask import Flask, request, jsonify
from deepface import DeepFace
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Emotion API Running"

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        if "image" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No image uploaded"
            })

        image = request.files["image"]

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        )

        image.save(temp.name)

        result = DeepFace.analyze(
            img_path=temp.name,
            actions=["emotion"],
            enforce_detection=False
        )

        emotion = result[0]["dominant_emotion"]

        os.remove(temp.name)

        return jsonify({
            "status": "success",
            "emotion": emotion
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )