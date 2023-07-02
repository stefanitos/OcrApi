import requests

# Specify the URL
url = 'http://127.0.0.1:8000/smite/ocr/upload'


bin_img = open('loading_screen.png', 'rb')

# Dict with post data
data = {"file": bin_img}

# Make the request
response = requests.post(url, files = data)

# Close the file to free resources
bin_img.close()

# Print the response
print(response.json())
