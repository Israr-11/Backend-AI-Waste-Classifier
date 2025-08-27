import hashlib
from io import BytesIO
import base64
from PIL import Image
import numpy as np
from fastapi import HTTPException, status
from services.mlModelService import predict_category 
from utils.uploadImage import upload_media
from utils.database import dBConnection
from datetime import datetime



def generate_image_hash(image_file) -> str:
    """
    Generate a unique hash for the uploaded image.
    """
    image = Image.open(image_file)
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    image_bytes = img_byte_arr.getvalue()
    image_hash = hashlib.sha256(image_bytes).hexdigest()  # GENERATING A HASH USING SHA-256
    return image_hash

def process_image(image_file) -> np.ndarray:
    """
    Preprocess the image (resize to 128x128 and normalize).
    """
    image = Image.open(image_file)
    image = image.resize((128, 128))  # RESIZING IMAGE TO 128X128
    img_array = np.array(image) / 255.0  # NORMALIZING THE IMAGE TO [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # ADDING BATCH DIMENSION
    return img_array

def get_recycling_instructions(category: str):
    """
    Fetch recycling instructions for the given category.
    Ensure that it does not create a new record if the category is missing.
    """
    try:
        collection_pred, collection_instructions, collection_feedback = dBConnection()
        recycling_data = collection_instructions.find_one({"category": category})

        if not recycling_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recycling instructions not found")

        return {
            "isWaste": recycling_data.get("isWaste"),
            "recyclable": recycling_data.get("recyclable"),
            "instructions": recycling_data.get("instructions")
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch recycling instructions")

def save_prediction(image_hash: str, predicted_category: str, image_url: str):
    """
    Save the prediction in the database.
    """
    try:
        collection_pred, collection_instructions, collection_feedback  = dBConnection()

        # SAVING PREDICTION IN THE PREDICTION COLLECTION

        #print(f"Saving prediction for image: {image_hash} and category: {predicted_category} ")
        prediction_data = {
            "image_hash": image_hash,
            "original_prediction": predicted_category,
            "correct_classification": predicted_category,
            "category": predicted_category,
            "image_url": image_url,
            "entryTime": datetime.now()

        }
        #print(f"Prediction data: {prediction_data}")
        collection_pred.insert_one(prediction_data)
    except Exception as e:
        #print(f"Error saving prediction: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save prediction")

def process_image_and_get_instructions(image_file) -> dict:
    """
    Process the uploaded image, check prediction, and return recycling instructions.
    """
     # Upload image to Cloudinary
    #print("Uploading image to Cloudinary...")
    upload_result = upload_media(image_file)
    #print(f"Upload result: {upload_result}")
    if not upload_result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload image")
    
    image_url = upload_result["url"]

    image_hash = generate_image_hash(image_file)
    #print(f"Image hash line 80: {image_hash}")
    # STEP 1: CHECK IF THE IMAGE ALREADY HAS A PREDICTION IN THE DATABASE
    collection_pred, collection_instructions, collection_feedback = dBConnection()
    existing_prediction =  collection_pred.find_one({"image_hash": image_hash})
    #print(f"Existing prediction: {existing_prediction}")

    if existing_prediction:
       category_pred = existing_prediction.get("original_prediction")
       category_correct = existing_prediction.get("correct_classification")

    # MAKE SURE CORRECT CLASSIFICATION IS VALID
       category = category_correct if category_correct else category_pred

       #print(f"Using category for instructions: {category}")

    # FETCH CORRECT RECYCLING INSTRUCTIONS
       recycling_instructions = get_recycling_instructions(category)

       return {"image_hash": image_hash, "recycling_instructions": recycling_instructions}


    # STEP 2: IF NO PREDICTION, SEND THE IMAGE TO ML MODEL FOR PREDICTION
    img_array = process_image(image_file)  # Preprocess image for ML model
    predicted_category = predict_category(img_array)  # Get the prediction from ML model
    print(f"Predicted category line 97: {predicted_category}")
    # STEP 3: SAVING PREDICTION IN THE PREDICTION TABLE
    save_prediction(image_hash, predicted_category, image_url)

    # STEP 4: FETCHING THE RECYCLING INSTRUCTIONS FOR THE PREDICTED CATEGORY
    recycling_instructions = get_recycling_instructions(predicted_category)
    print(f"Recycling instructions for {predicted_category} line 124: {recycling_instructions}")
    return {"image_hash": image_hash, "image_url": image_url, "recycling_instructions": recycling_instructions}
