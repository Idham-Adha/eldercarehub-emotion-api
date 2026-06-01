from flask import Flask, request, jsonify
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Emotion API Running"

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        # Import DeepFace hanya apabila endpoint dipanggil
        from deepface import DeepFace

        if "image" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No image uploaded"
            }), 400

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

        # Padam fail sementara
        if os.path.exists(temp.name):
            os.remove(temp.name)

        return jsonify({
            "status": "success",
            "emotion": emotion
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
