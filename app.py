# import codon
import io
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as image_utils
# from tensorflow.keras.applications import vgg16
from tensorflow.keras.applications import efficientnet


app = Flask(__name__)
model = load_model('03-acuracia-80_26-Enet.h5')
feature_extraction_model = efficientnet.EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

class_labels = [
        'Art Déco',
        'Art Nouveau',
        'Barroca',
        'Contemporânea',
        'Eclética',
        'Egípcia',
        'Gótica',
        'Grega',
        'Islâmica',
        'Japonesa',
        'Moderna',
        'Pós-Moderna',
        'Renascentista'
    ]


# @codon.jit(pyvars=['image_utils', 'np', 'efficientnet', 'Image', 'io'])
def preprocess_image(image):
    img = Image.open(io.BytesIO(image)).resize((224, 224))
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    image_array = image_utils.img_to_array(img)
    images = np.expand_dims(image_array, axis=0)
    return efficientnet.preprocess_input(images)


# @codon.jit(pyvars=['preprocess_image', 'np', 'class_labels'])
def classify_architecture(image, model, feature_extraction_model):
    """Classify the architecture style in the given image using the provided models."""
    preprocessed_image = preprocess_image(image)
    features = feature_extraction_model.predict(preprocessed_image)
    results = model.predict(features)
    single_result = results[0]
    most_likely_class_index = int(np.argmax(single_result))
    class_likelihood = single_result[most_likely_class_index]
    class_label = class_labels[most_likely_class_index]

    return class_label, float(class_likelihood)


@app.route('/classify', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image'].read()
    class_label, class_likelihood = classify_architecture(image, model, feature_extraction_model)

    response = {
        'architecture': class_label,
        'likelihood': float(class_likelihood)
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
