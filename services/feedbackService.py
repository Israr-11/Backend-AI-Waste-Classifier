from fastapi import HTTPException, status
from utils.database import dBConnection
from models.feedback import UserFeedBack  

# Define techniques categories
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
        
        # Always store the feedback
        collection_feedback.insert_one(feedback_data)
        
        response = {"status": "SUCCESSFUL"}
        
        if feedback_data["is_correct"] == True:
            # User confirmed the prediction was correct
            response["message"] = "Feedback saved successfully. Thank you for confirming our prediction!"
        else:
            # User indicated the prediction was incorrect
            # Update the prediction collection with the correct category
            collection_pred.update_one(
                {"image_hash": feedback_data["image_hash"]},
                {"$set": {"correct_classification": feedback_data["correct_category"]}}
            )
            
            # Get the original prediction for comparison
            original_prediction = collection_pred.find_one({"image_hash": feedback_data["image_hash"]})
            
            if original_prediction:
                # Get techniques the user has already tried
                tried_before = feedback_data.get("tried_techniques", [])
                
                # Filter out techniques they've already tried
                untried_preprocessing = [tech for tech in PREPROCESSING_TECHNIQUES if tech not in tried_before]
                untried_new_photo = [tech for tech in NEW_PHOTO_TECHNIQUES if tech not in tried_before]
                
                # Create messages for each category
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
                
                # Combine messages
                if preprocessing_message and new_photo_message:
                    full_message = f"Thank you for the correction! {preprocessing_message}\n\n{new_photo_message}"
                elif preprocessing_message:
                    full_message = f"Thank you for the correction! {preprocessing_message}"
                elif new_photo_message:
                    full_message = f"Thank you for the correction! {new_photo_message}"
                else:
                    full_message = "Thank you for the correction! You've tried all our suggested techniques."
                
                # Add image quality improvement suggestions
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
