import tensorflow as tf
from tensorflow.keras.applications import mobilenet_v2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np
from PIL import Image

# Loading the pre-trained MobileNetV2 model + weights trained on ImageNet
model = mobilenet_v2.MobileNetV2(weights='imagenet')


def prepare_image(img_path):
    """Loads and preprocesses an image for MobileNetV2."""
    img = image.load_img(img_path, target_size=(224, 224)) # MobileNetV2 expects 224x224 images
    img_array = image.img_to_array(img) 
    img_array_expanded = np.expand_dims(img_array, axis=0) # Add batch dimension
    return preprocess_input(img_array_expanded) # Use MobileNetV2's specific preprocessing

def predict_image_class(img_path):
    """Loads an image, preprocesses it, and predicts its class using MobileNetV2."""
    try:
        # Load the pre-trained MobileNetV2 model
        model = mobilenet_v2.MobileNetV2(weights='imagenet')

        # Prepare the image
        processed_image = prepare_image(img_path)

        # Make prediction
        predictions = model.predict(processed_image)

        # Decode the prediction into human-readable labels and gets top 3 predictions 
        decoded = decode_predictions(predictions, top=3)[0] 

        print(f"Predictions for {img_path}:")
        for i, (imagenet_id, label, score) in enumerate(decoded):
            print(f"{i+1}: {label} ({score:.2f})")
        return decoded # Return the decoded predictions

    except FileNotFoundError:
        print(f"Error: Image file not found at {img_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#Examples
if __name__ == "__main__":
    # Replace 'sample_images/cat_2.jpg' with the actual path to one of your images
    image_path_to_test = r'Your_File_Path\sample_images\cat_2.jpg'
    predict_image_class(image_path_to_test)

    # Replace 'sample_images/dog_2.jpg' with the actual path to another image
    image_path_to_test_2 = r'Your_File_Path\sample_images\dog_2.jpg'
    predict_image_class(image_path_to_test_2)