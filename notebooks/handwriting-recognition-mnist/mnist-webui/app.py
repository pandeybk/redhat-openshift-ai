import base64
import io

from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import requests as req  # For calling your OVMS endpoint

app = Flask(__name__)

# Your OVMS endpoint URL (change if needed):
ENDPOINT_URL = "https://mnist-v2-netsentinel.apps.cloud.xtoph152.dfw.ocp.run/v2/models/mnist-v2/infer"

@app.route("/")
def index():
    # Serve up the index.html by default
    return app.send_static_file("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Receives a JSON payload with a Base64-encoded PNG from the canvas,
    calls the model server, returns predicted digit as JSON.
    """
    data = request.get_json()
    if "image" not in data:
        return jsonify({"error": "No image data provided"}), 400

    # Data URL looks like "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA..."
    # We only want the Base64 part after the comma
    base64_image = data["image"].split(",")[1]

    # Decode the Base64 string into bytes
    image_bytes = base64.b64decode(base64_image)

    # Convert bytes into a Pillow Image (grayscale)
    img = Image.open(io.BytesIO(image_bytes)).convert("L")

    # 1) Resize to 28x28 (typical MNIST input size)
    img = img.resize((28, 28))

    # OPTIONAL: Save for debugging (so you can see what the server receives)
    img.save("debug_out.png")  # White digit on black background if everything is correct

    # 2) Convert the raw grayscale image to NumPy array, normalize to [0..1]
    arr = np.array(img, dtype=np.float32) / 255.0  # shape (28,28)

    # 3) Reshape to (1, 28, 28, 1) for the model
    arr = arr.reshape((1, 28, 28, 1))

    # Prepare the payload for OVMS (KFServing V2 protocol)
    data_list = arr.flatten().tolist()
    request_payload = {
        "inputs": [
            {
                "name": "inputs",            # adjust if your model has a different input name
                "shape": [1, 28, 28, 1],
                "datatype": "FP32",
                "data": data_list
            }
        ]
    }

    # Call the model server
    response = req.post(ENDPOINT_URL, json=request_payload, verify=False)
    if response.status_code != 200:
        return jsonify({
            "error": "Inference request failed",
            "details": response.text
        }), 500

    # Parse the response and get predicted class
    resp_json = response.json()
    output_data = resp_json["outputs"][0]["data"]
    output_array = np.array(output_data).reshape(1, -1)
    predicted_class = int(np.argmax(output_array, axis=1)[0])

    return jsonify({"predicted_class": predicted_class})

if __name__ == "__main__":
    # Run the Flask app (default port 5000)
    app.run(debug=True)
