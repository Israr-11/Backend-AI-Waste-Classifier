import cloudinary
import cloudinary.uploader
from fastapi import HTTPException
import os
from dotenv import load_dotenv

def setup_cloudinary():
    load_dotenv()
    
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )

def upload_media(file) -> dict:
    try:
        setup_cloudinary()
        
        # GET THE FILE CONTENT DIRECTLY
        result = cloudinary.uploader.upload(
            file,
            folder="uploads"  # THIS CREATES/USES A FOLDER IN CLOUDINARY
        )
        
        return {
            "success": True,
            "url": result.get('secure_url')
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
