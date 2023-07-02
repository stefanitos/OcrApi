from pytesseract import image_to_string
from PIL import Image
import cv2
import time

start_time = time.time()

offset_x = 180
offset_y_ally = 75
offset_y_enemy = 580
width = 150
height = 24
gap = 200

img = cv2.imread("loading_screen.png")
img = cv2.bitwise_not(img)
img = Image.fromarray(img)

ally_players_coords = [(offset_x + (width + gap) * i, offset_y_ally, offset_x + (width + gap) * i + width, offset_y_ally + height) for i in range(5)]
enemy_players_coords = [(offset_x + (width + gap) * i, offset_y_enemy, offset_x + (width + gap) * i + width, offset_y_enemy + height) for i in range(5)]
all_players_coords = ally_players_coords + enemy_players_coords

players = {
    "ally": [],
    "enemy": []
}

for i, box in enumerate(all_players_coords):
    cropped_img = img.crop(box)
    # cropped_img.save(f"players/player{i+1}.png")
    text = image_to_string(cropped_img, config="--psm 7").strip()

    if text:
        if i < 5:
            players["ally"].append(text)
        else:
            players["enemy"].append(text)


print(players)
