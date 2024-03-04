import requests
import json
import zipfile
import io

# SEND A NO-IMAGE REQUEST



# The URL where your Flask app is running
url = 'http://localhost:5000/process_image_sequence'

# The operations you want to perform
operations = json.dumps([
    {"operation": "rotate", "degrees": 90},
    {"operation": "thumbnail"} 
])

# Define the request payload with no image file included
data = {'operations': operations}

# Send the POST request without an image file
response = requests.post(url, data=data)

# Check the response status code
if response.status_code == 200:
    # The response is a ZIP file; we need to extract it
    zip_in_memory = io.BytesIO(response.content)
    with zipfile.ZipFile(zip_in_memory) as zf:
        # Extract all files into a directory (e.g., "./processed_images/")
        zf.extractall(path="./processed_images/")
    print("The processed images are saved in './processed_images/'.")
else:
    # Expected to print error message due to missing image file
    print(f"Error: {response.status_code}")
    print(response.text)
