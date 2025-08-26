import tensorflow as tf
import numpy as np
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


# LOADING THE TRAINED MODEL
model_path = os.path.join(os.getcwd(), 'machineLearning', 'waste_classification_model_v2.keras')
model = tf.keras.models.load_model(model_path)

class_names = ['ewaste', 'glass', 'metal', 'organic', 'paper', 'plastic', 'trash']

def predict_category(img_array: np.ndarray) -> tuple:
    """
    Given a preprocessed image array, make a prediction using the trained ML model.
    Returns the predicted class and the model's confidence score.
    """
    # PREDICTING THE CLASS USING THE MODEL
    prediction = model.predict(img_array)
    
    # GETTING THE PREDICTED CLASS AND CONFIDENCE (PROBABILITY)
    predicted_class = class_names[np.argmax(prediction)]
    #confidence = np.max(prediction)  # Confidence of the predicted class
    
    #return predicted_class, confidence
    return predicted_class

