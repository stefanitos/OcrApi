from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from PIL import Image
import pytesseract
import cv2
import numpy as np
import io
import uvicorn
import time

app = FastAPI()

offset_x = 180
offset_y_ally = 75
offset_y_enemy = 580
width = 150
height = 24
gap = 200


class Players(BaseModel):
    ally: list[str]
    enemy: list[str]


async def get_player_names(img: Image) -> Players:
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = cv2.bitwise_not(img)
    img = Image.fromarray(img)

    ally_players_coords = [
        (offset_x + (width + gap) * i, offset_y_ally, offset_x + (width + gap) * i + width, offset_y_ally + height) for
        i in range(5)]
    enemy_players_coords = [
        (offset_x + (width + gap) * i, offset_y_enemy, offset_x + (width + gap) * i + width, offset_y_enemy + height)
        for i in range(5)]
    all_players_coords = ally_players_coords + enemy_players_coords

    players = {"ally": [], "enemy": []}

    for i, box in enumerate(all_players_coords):
        cropped_img = img.crop(box)
        text = pytesseract.image_to_string(cropped_img, config="--psm 7").strip()
        text = "".join([c for c in text if c.isalpha() or c.isdigit()])

        if text:
            if i < 5:
                players["ally"].append(text)
            else:
                players["enemy"].append(text)

    return Players(**players)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/ocr/smite/upload")
async def smite_upload(file: UploadFile = File(...)):
    start_time = time.time()
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))

        # img.save("test.png")
        players = await get_player_names(img)
        end_time = time.time()
        time_taken = end_time - start_time
        return {"players": players, "time_taken": time_taken}
    except Exception as e:
        return {"players": {"ally": [], "enemy": []}, "time_taken": 0}


@app.get("/ocr/upload", response_class=HTMLResponse)
async def upload_form():
    return """
    <html>
        <body>
            <form action="/ocr/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit">
            </form>
        </body>
    </html>
    """

@app.post("/ocr/upload")
async def ocr_upload(file: UploadFile = File(...)):
    start_time = time.time()
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(img)
        end_time = time.time()
        time_taken = end_time - start_time
        return HTMLResponse(f"""
        <html>
            <body>
                <h1>Extracted Text</h1>
                <p>{text}</p>
                <p>Time taken: {time_taken} seconds</p>
            </body>
        </html>
        """)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
