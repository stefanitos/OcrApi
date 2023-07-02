from pytesseract import image_to_string
from PIL import Image


for i in range(10):
    img = Image.open(f"players/player{i+1}.png")
    text = image_to_string(img, config='--psm 7 --oem 3')
    print(f"player{i+1}: {text}")


# with Image.open('players/player3.png') as img:
#     text = image_to_string(img)
#     print(text)
    
