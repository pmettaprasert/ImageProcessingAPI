from flask import Flask, request, send_file, jsonify, make_response
from OpenCV.ProcessingService import process_image_sequence
from werkzeug.exceptions import BadRequest
import json

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
        processed_image_stream = process_image_sequence(image_file, operations)

        # Create a response object and manually set the headers
        response = make_response(processed_image_stream.getvalue())
        response.headers.set('Content-Type', 'image/jpeg')
        response.headers.set('Content-Disposition', 'attachment', filename='processed_image.jpg')
        return response
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


