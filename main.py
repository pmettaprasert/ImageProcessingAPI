from flask import Flask, request, send_file, jsonify
import json
import io
import zipfile
from OpenCV.ProcessingService import process_image_sequence
from werkzeug.exceptions import BadRequest
from PIL import Image

app = Flask(__name__)

@app.route('/process_image_sequence', methods=['POST'])
def process_image_sequence_route():
    if 'image' not in request.files:
        raise BadRequest("Image file is missing in the request.")
    if 'operations' not in request.form:
        raise BadRequest("Operations data is missing in the request.")

    try:
        image_file = request.files['image'].read()
        
        
        #TODO NEED TO CHECK MISSING PARAMETERS
        #check if image is JPG, PNG, GIF, TIFF
        
        # Check if image is JPG, PNG, GIF, or TIFF
        image = Image.open(io.BytesIO(image_file))
        image_format = image.format
        if image_format not in ['JPEG', 'PNG', 'GIF', 'TIFF']:
            raise BadRequest("Invalid image format. Only JPG, PNG, GIF, and TIFF are supported.")
        operations = json.loads(request.form['operations'])
        for op in operations:
            check_op_parameters(op)
        
        # Process image and get list of (filename, bytes) for processed images
        processed_images = process_image_sequence(image_file, operations)
        
        # Log the number of operations
        app.logger.info(f"Processed the image with {len(operations)} operations")
        #log the operations performed
        app.logger.info(f"Operations performed: {operations}")

        # Create a ZIP archive in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add processed images to the ZIP, iterating over each image
            for filename, img_bytes in processed_images:
                zf.writestr(filename, img_bytes)
                
        # Log the creation of the ZIP archive
        app.logger.info("Created ZIP archive")

        # Reset the pointer of the BytesIO object to the beginning
        memory_file.seek(0)

        # Create and return the response object for sending the ZIP file
        response = send_file(memory_file,
                     mimetype='application/zip',
                     as_attachment=True,
                     download_name='processed_images.zip')
        
        app.logger.info("Returning the ZIP archive")

        return response
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        #if it is a value error, return a 400 error
        if isinstance(e, ValueError):
            raise BadRequest(str(e))
        #else it is a 500 error
        raise BadRequest("An error occurred while processing the image")
    
    
def check_op_parameters(operation):
    operation_type = operation.get('operation')

    # Define required parameters for each operation type
    required_params = {
        'flip': ['direction'],
        'rotate': ['degrees'],
        'resize': ['percentage'],
        # 'thumbnail', 'grayscale', 'rotateLeft', 'rotateRight' do not have required params in this setup
    }

    # Check if operation type is known and has required parameters
    if operation_type in required_params:
        for param in required_params[operation_type]:
            if param not in operation:
                raise ValueError(f"'{param}' is required for {operation_type} operation.")
            # Additional specific checks can be implemented here
            if operation_type == 'flip' and operation[param] not in ['horizontal', 'vertical']:
                raise ValueError("Flip direction must be 'horizontal' or 'vertical'.")
            if operation_type == 'rotate':
                degrees = operation.get('degrees', 0)
                if not -10000 <= degrees <= 10000:
                    raise ValueError("Rotation degrees must be between -10000 and +10000.")
            if operation_type == 'resize':
                percentage = operation.get('percentage', 100)
                if not -95 <= percentage <= 500:
                    raise ValueError("Resize percentage must be between -95% and +500%.")

    else:
        raise ValueError(f"Unknown operation type: {operation_type}")

    
    
    
    

if __name__ == '__main__':
    app.run(debug=True)
