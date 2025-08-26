from fastapi import APIRouter, HTTPException, status
from models.feedback import UserFeedBack
from services.feedbackService import save_feedback

router = APIRouter()

@router.post("/feedback", response_model=dict)
async def submit_feedback(feedback: UserFeedBack):
    """
    Endpoint to submit user feedback and get appropriate response.
    """
    try:
        result = save_feedback(feedback)
        print(f"Feedback submitted: {result}")
        return result

    except Exception as e:
        print(f"An error occurred while submitting form: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to Submit Feedback"
        )
