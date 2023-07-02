from pytesseract import image_to_string
from PIL import Image
import cv2

# change tessedit_write_images to 1 in C:\Program Files\Tesseract-OCR\tessdata\configs\tsv

offset_x = 180
offset_y_ally = 75
offset_y_enemy = 580
width = 150
height = 24
gap = 200

img = cv2.imread("loading_screen.png")
# OCR 4.x -> black text on white background is better
img = cv2.bitwise_not(img)
img = Image.fromarray(img)

ally_players_coords = [(offset_x + (width + gap) * i, offset_y_ally, offset_x + (width + gap) * i + width, offset_y_ally + height) for i in range(5)]
enemy_players_coords = [(offset_x + (width + gap) * i, offset_y_enemy, offset_x + (width + gap) * i + width, offset_y_enemy + height) for i in range(5)]
all_players_coords = ally_players_coords + enemy_players_coords

for i, box in enumerate(all_players_coords):
    cropped_img = img.crop(box)
    cropped_img.save(f"players/player{i+1}.png")