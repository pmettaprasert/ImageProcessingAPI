from flask import Flask, request, send_file, jsonify
import json
import io
import zipfile
from OpenCV.ProcessingService import process_image_sequence
from werkzeug.exceptions import BadRequest
from PIL import Image

app = Flask(__name__)

# Define a maximum image size (in bytes)
MAX_IMAGE_SIZE = 5 * 1024 * 1024  
MAX_SIZE_IN_MB = MAX_IMAGE_SIZE / (1024 * 1024)
MAX_OPERATIONS = 20

@app.route('/process_image_sequence', methods=['POST'])
def process_image_sequence_route():
    try:
        # Preliminary checks
        if 'image' not in request.files:
            raise BadRequest("Image file is missing in the request.")
        if 'operations' not in request.form:
            raise BadRequest("Operations data is missing in the request.")
        if request.content_length > MAX_IMAGE_SIZE:
            raise BadRequest(f"Image file is too large. Maximum allowed is {MAX_SIZE_IN_MB} MB.")

        image_file = request.files['image'].read()

        # Image format check
        image = Image.open(io.BytesIO(image_file))
        image_format = image.format
        if image_format not in ['JPEG', 'PNG', 'GIF', 'TIFF']:
            raise BadRequest(f"Invalid image format. Image was {image_format}. Only JPG, PNG, GIF, and TIFF are supported.")

        # Operations count check
        operations = json.loads(request.form['operations'])
        if len(operations) > MAX_OPERATIONS:
            raise BadRequest(f"Too many operations. Maximum allowed is {MAX_OPERATIONS}.")
        
        for index, op in enumerate(operations, start=1):
            check_op_parameters(op, index)

        # Process image
        processed_images = process_image_sequence(image_file, operations)

        # Create ZIP archive in memory for processed images
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename, img_bytes in processed_images:
                zf.writestr(filename, img_bytes)
        memory_file.seek(0)

        return send_file(memory_file, mimetype='application/zip', as_attachment=True, download_name='processed_images.zip')

    except BadRequest as br:
        # Handle known client errors first
        app.logger.error(f"Client error: {str(br)}")
        return jsonify({'error': str(br)}), 400
    except Exception as e:
        # Handle unexpected errors
        app.logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({'error': "An unexpected error occurred while processing the image"}), 500
    
    
def check_op_parameters(operation, index):
    operation_type = operation.get('operation')

    # Define required parameters for each operation type
    required_params = {
        'flip': ['direction'],
        'rotate': ['degrees'],
        'resize': ['percentage'],
        # Assuming 'thumbnail', 'grayscale', 'rotateLeft', 'rotateRight' do not have required params
    }

    if operation_type in required_params:
        for param in required_params[operation_type]:
            if param not in operation:
                raise BadRequest(f"Operation {index}: '{param}' is required for {operation_type} operation. Please check your spelling or syntax.")

            # Additional specific checks
            if operation_type == 'flip':
                direction = operation[param]
                if direction not in ['horizontal', 'vertical']:
                    raise BadRequest(f"Operation {index}: Flip direction must be 'horizontal' or 'vertical'.")
            
            if operation_type == 'rotate':
                degrees = operation[param]
                if not isinstance(degrees, int):
                    raise BadRequest(f"Operation {index}: Rotation degrees must be an integer.")
                if not -10000 <= degrees <= 10000:
                    raise BadRequest(f"Operation {index}: Rotation degrees must be between -10000 and +10000.")
            
            if operation_type == 'resize':
                percentage = operation[param]
                if not isinstance(percentage, int) and not isinstance(percentage, float):
                    raise BadRequest(f"Operation {index}: Resize percentage must be an integer or float.")
                if not -95 <= percentage <= 500:
                    raise BadRequest(f"Operation {index}: Resize percentage must be between -95% and +500%.")
                
    elif operation_type in ['thumbnail', 'grayscale', 'rotateLeft', 'rotateRight']:
        # No required parameters for these operations
        pass

    else:
        raise BadRequest(f"Operation {index}: Unknown operation type: {operation_type}. Please check the operation type and parameters.")
    

    
    
    
    

if __name__ == '__main__':
    app.run(debug=True)
