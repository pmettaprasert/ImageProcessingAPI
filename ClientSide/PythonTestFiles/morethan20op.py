import requests
import json
import zipfile
import io

# The URL where your Flask app is running
url = 'http://localhost:5000/process_image_sequence'

# The path to the image you want to process
image_path = 'ClientSide\PythonTestFiles\differentformatting\profile.jpg'  # Replace with your image path

# The operations you want to perform
operations = json.dumps([
    # Multiply by 30 which is more than 20 operations allowed
    {"operation": "rotate", "degrees": 30} for _ in range(30)
])

# Open the image file in binary mode
with open(image_path, 'rb') as image_file:
    # Define the request payload
    files = {'image': image_file}
    data = {'operations': operations}
    
    # Send the POST request
    response = requests.post(url, files=files, data=data)
    
    # Check the response status code
    if response.status_code == 200:
        # The response is a ZIP file; we need to extract it
        zip_in_memory = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_in_memory) as zf:
            # Extract all files into a directory (e.g., "./processed_images/")
            zf.extractall(path="./processed_images/")
        print("The processed images are saved in './processed_images/'.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
