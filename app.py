from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
import pytesseract


app = FastAPI()


@app.get("ocr/upload")
async def upload(request: Request):
    # Get the image from the request and check if its allowed ['png', 'jpg', 'jpeg']
    image = request.files["image"]
    if image.filename.split(".")[-1] not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")
    # Read the image and convert it to text
    text = pytesseract.image_to_string(image.file.read())