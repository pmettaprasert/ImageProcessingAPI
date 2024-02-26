from flask import Flask, request, send_file, jsonify, make_response
import json
import io
import zipfile

# Assuming process_image_sequence is updated accordingly
from OpenCV.ProcessingService import process_image_sequence
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

@app.route('/process_image_sequence', methods=['POST'])
def process_image_sequence_route():
    if 'image' not in request.files:
        raise BadRequest("Image file is missing in the request.")
    if 'operations' not in request.form:
        raise BadRequest("Operations data is missing in the request.")

    try:
        image_file = request.files['image'].read()
        operations = json.loads(request.form['operations'])

        # Assuming process_image_sequence now returns a list of (filename, bytes) tuples
        images = process_image_sequence(image_file, operations)
        
        # Log the number of operations
        app.logger.info(f"Processed the image with {len(operations)} operations")

        # Create a ZIP archive in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add images to the ZIP, iterating over each image
            for filename, img_bytes in images:
                zf.writestr(filename, img_bytes)
                
        # Log the creation of the ZIP archive
        app.logger.info("Created ZIP archive")

        # Go to the start of the BytesIO object
        memory_file.seek(0)

        # Create a response object for sending the ZIP file
        response = send_file(memory_file, attachment_filename='processed_images.zip', as_attachment=True)
        response.headers['Content-Type'] = 'application/zip'
        
        app.logger.info("Returning the ZIP archive")

        return response
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
