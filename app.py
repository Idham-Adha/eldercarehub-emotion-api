from flask import Flask, request, jsonify
import tempfile
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "Emotion API Running", 200


@app.route("/health")
def health():
    return "OK", 200


@app.route("/analyze", methods=["POST"])
def analyze():

    temp_file = None

    try:

        # Import DeepFace hanya apabila endpoint dipanggil
        from deepface import DeepFace

        if "image" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No image uploaded"
            }), 400

        image = request.files["image"]

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        )

        image.save(temp_file.name)

        result = DeepFace.analyze(
            img_path=temp_file.name,
            actions=["emotion"],
            enforce_detection=False
        )

        emotion = result[0]["dominant_emotion"]

        return jsonify({
            "status": "success",
            "emotion": emotion
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:

        if temp_file and os.path.exists(temp_file.name):
            os.remove(temp_file.name)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port
    )
