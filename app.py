import tensorflow as tf
from tensorflow.keras.applications import mobilenet_v2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np
from PIL import Image
import io # This is to handle image data in memory

from flask import Flask, request, jsonify # Importing Flask classes

# Initializing Flask app
app = Flask(__name__)

# Load the model. Do this once when the app starts.
# Make sure this model is accessible globally within the app context
model = None
def load_model():
    global model
    model = mobilenet_v2.MobileNetV2(weights='imagenet')
    print("Model loaded for the API!")

def prepare_image_from_bytes(img_bytes):
    """Loads and preprocesses image data received via API."""
    img = Image.open(io.BytesIO(img_bytes))
    if img.mode != 'RGB': # Ensure image is RGB, MobileNetV2 expects 3 channels
        img = img.convert('RGB')
    img = img.resize((224, 224)) # Resize to MobileNetV2's expected input size
    img_array = image.img_to_array(img)
    img_array_expanded = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array_expanded)

# Define the prediction endpoint
@app.route('/predict', methods=['POST']) # Endpoint accessible via POST request at /predict
def handle_prediction():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400 # Bad request

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # Read image file bytes
            img_bytes = file.read()

            # Prepare image
            processed_image = prepare_image_from_bytes(img_bytes)

            # Make prediction (use the globally loaded model)
            predictions = model.predict(processed_image)
            decoded = decode_predictions(predictions, top=3)[0]

            # Format response
            result = []
            for i, (imagenet_id, label, score) in enumerate(decoded):
                result.append({'label': label, 'score': float(score)}) # Convert score to float for JSON

            return jsonify({'predictions': result}) # Return predictions as JSON

        except Exception as e:
            print(f"Error processing file: {e}") # Log error server-side
            return jsonify({'error': 'Failed to process image'}), 500 # Internal server error
    else:
        return jsonify({'error': 'Invalid file'}), 400
    
# Execution 
if __name__ == '__main__':
    print("Starting Flask app...")
    load_model() # Load the model before starting the server
    # Run the app (accessible only on your machine for now)
    # Use host='0.0.0.0' to make it accessible from other devices on your network. This will be useful for Docker later.
    app.run(debug=True, host='0.0.0.0', port=5000) # debug=True helps with development
