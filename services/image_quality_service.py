import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64

def enhance_image(image: Image.Image) -> Image.Image:
    """
    Enhances image quality using OpenCV.
    - Bounding box to crop the image to the region of interest
    - Converts the image to grayscale
    - Applies histogram equalization
    - Enhances sharpness using an unsharp mask filter
    """
    #BOUNDING BOX
    image_cv = cv2.boxFilter(image, -1, (5, 5), normalize=True)
    
    image_cv = np.array(image)
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)  

    # COVERT TO GRAYSCALE
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # HISTOGRAM EQUALIZATION
    equalized = cv2.equalizeHist(gray)

    # SHARPENING
    enhanced_image = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

    # SHARPENING FILTER
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(enhanced_image, -1, kernel)

    # CONVERT BACK TO PIL IMAGE
    return Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))

def calculate_clarity(image: Image.Image) -> float:
    """
    Estimates image clarity using the Laplacian variance method.
    A higher variance means a sharper image.
    """
    image_cv = np.array(image.convert("L"))  
    variance = cv2.Laplacian(image_cv, cv2.CV_64F).var()  
    return variance

def validate_image(image: Image.Image, clarity_threshold: float = 100.0) -> bool:
    """
    Checks if the image clarity is above the defined threshold.
    Returns True if the image is clear enough, False otherwise.
    """
    clarity_score = calculate_clarity(image)
    return clarity_score >= clarity_threshold

def prepare_image_for_model(image: Image.Image) -> str:
    """
    Enhances and validates an image before sending it to the ML model.
    Returns the base64 string of the processed image.
    """
    # ENHANCING IMAGE QUALITY
    enhanced_image = enhance_image(image)

    # CHECKING CLARITY BEFORE SENDING
    if not validate_image(enhanced_image):
        raise ValueError("Image clarity is too low. Please upload a clearer image.")

    # CONVERTING TO BASE64
    buffered = BytesIO()
    enhanced_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
