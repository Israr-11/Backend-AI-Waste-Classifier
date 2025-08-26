from fastapi import HTTPException, status
from utils.database import dBConnection
from models.feedback import UserFeedBack  

PREPROCESSING_TECHNIQUES = [
  "Adjust brightness",
  "Adjust contrast",
  "Apply grayscale filter",
  "Apply sepia filter",
  "Crop the image"
]

NEW_PHOTO_TECHNIQUES = [
  "Take photos in good lighting conditions",
  "Ensure the waste item is centered in the frame",
  "Use a plain background when possible",
  "Avoid blurry images by holding your device steady",
  "Try different angles if the item has distinctive features",
  "Clean the item before photographing",
  "Remove packaging or labels if possible"
]

def save_feedback(feedback: UserFeedBack):
    """
    Save user feedback in the database and provide appropriate response.
    """
    try:
        collection_pred, collection_instructions, collection_feedback = dBConnection()
        
        feedback_data = feedback.to_dict()
        print(f"Feedback data: {feedback_data}")

        # SAVING THE FEEDBACK
        collection_feedback.insert_one(feedback_data)
        
        response = {"status": "SUCCESSFUL"}
        
        if feedback_data["is_correct"] == True:
            # USER CONFIRMED THE PREDICTION WAS CORRECT
            response["message"] = "Feedback saved successfully. Thank you for confirming our prediction!"
        else:
            # USER INDICATED THE PREDICTION WAS INCORRECT
            # UPDATING THE PREDICTION COLLECTION WITH THE CORRECT CATEGORY
            collection_pred.update_one(
                {"image_hash": feedback_data["image_hash"]},
                {"$set": {"correct_classification": feedback_data["correct_category"]}}
            )
            
            # GETTING THE ORIGINAL PREDICTION FOR COMPARISON
            original_prediction = collection_pred.find_one({"image_hash": feedback_data["image_hash"]})
            
            if original_prediction:
                # GET TECHNIQUES THE USER HAS ALREADY TRIED
                tried_before = feedback_data.get("tried_techniques", [])
                
                # FILTERING OUT TECHNIQUES THEY'VE ALREADY TRIED
                untried_preprocessing = [tech for tech in PREPROCESSING_TECHNIQUES if tech not in tried_before]
                untried_new_photo = [tech for tech in NEW_PHOTO_TECHNIQUES if tech not in tried_before]

                # CREATING MESSAGES FOR EACH CATEGORY
                preprocessing_message = ""
                if untried_preprocessing:
                    preprocessing_message = "Try these adjustments to your current image:\n"
                    for i, technique in enumerate(untried_preprocessing, 1):
                        preprocessing_message += f"{i}. {technique}. "
                
                new_photo_message = ""
                if untried_new_photo:
                    new_photo_message = "For better results, consider taking a new photo with these tips:\n"
                    for i, technique in enumerate(untried_new_photo, 1):
                        new_photo_message += f"{i}. {technique}. "
                
                # COMBINING MESSAGES
                if preprocessing_message and new_photo_message:
                    full_message = f"Thank you for the correction! {preprocessing_message}\n\n{new_photo_message}"
                elif preprocessing_message:
                    full_message = f"Thank you for the correction! {preprocessing_message}"
                elif new_photo_message:
                    full_message = f"Thank you for the correction! {new_photo_message}"
                else:
                    full_message = "Thank you for the correction! You've tried all our suggested techniques."

                # ADDING IMAGE QUALITY IMPROVEMENT SUGGESTIONS
                response["message"] = full_message
                response["original_category"] = original_prediction.get("original_prediction")
                response["corrected_category"] = feedback_data["correct_category"]
                response["tried_techniques"] = tried_before
                response["untried_preprocessing"] = untried_preprocessing
                response["untried_new_photo"] = untried_new_photo
            else:
                response["message"] = "Feedback saved successfully, but we couldn't find the original prediction."
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save feedback: {str(e)}"
        )
