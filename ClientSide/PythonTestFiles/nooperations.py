import requests
import zipfile
import io

# The URL where your Flask app is running
url = 'http://localhost:5000/process_image_sequence'

# The path to the image you want to process
image_path = 'ClientSide\PythonTestFiles\differentformatting\profile.jpg'  # Replace with your image path

# Open the image file in binary mode
with open(image_path, 'rb') as image_file:
    # Define the request payload with only the image file, no 'operations' data
    files = {'image': image_file}
    
    # Send the POST request without 'operations'
    response = requests.post(url, files=files)
    
    # Check the response status code
    if response.status_code == 200:
        # If the server somehow handles requests with no operations specified
        # The response is expected to be a ZIP file; we need to extract it
        zip_in_memory = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_in_memory) as zf:
            # Extract all files into a directory (e.g., "./processed_images/")
            zf.extractall(path="./processed_images/")
        print("The processed images are saved in './processed_images/'.")
    else:
        # Likely error due to missing 'operations' data
        print(f"Error: {response.status_code}")
        print(response.text)
