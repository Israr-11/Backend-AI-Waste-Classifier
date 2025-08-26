from fastapi import APIRouter, UploadFile, File, HTTPException, status
from services.imageProcessingService import process_image_and_get_instructions  # Importing the service

router = APIRouter()

@router.post("/upload_image", response_model=dict)
async def upload_image(image_file: UploadFile = File(...)) -> dict:
    try:
        # CALLING THE SERVICE TO PROCESS IMAGE AND GET RECYCLING INSTRUCTIONS
        print("Received image for processing...")
        result = process_image_and_get_instructions(image_file.file)
        print(f"Result in imageProcessingController: {result}")
        
        response = {
            "message": "Image uploaded and processed successfully",
            "image_hash": result.get("image_hash"),
            "image_url": result.get("image_url"),
            "status": "SUCCESSFUL",
            "recycling_instructions": result.get("recycling_instructions")  # Returning the recycling instructions
        }

        return response

    except Exception as e:
        print(f"An error occurred while uploading image: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload image")
