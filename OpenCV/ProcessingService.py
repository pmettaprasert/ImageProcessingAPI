import numpy as np
import cv2
import io

# Import your image processing classes
from .ImageProcessor import FlipProcessor, RotateProcessor, GrayscaleProcessor, ResizeProcessor, ThumbnailProcessor, RotateLeftProcessor, RotateRightProcessor

def convert_direction_to_code(direction):
    if direction == 'horizontal':
        return 1
    elif direction == 'vertical':
        return 0

def process_image_sequence(image_bytes, operations):
    # Convert the bytes to an OpenCV image
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    # Process the image with the sequence of operations
    for op in operations:
        operation_type = op['operation']
        
        if operation_type == 'flip':
            direction = op.get('direction')
            flip_code = convert_direction_to_code(direction)
            image = FlipProcessor(image, flip_code).process_image().get_image()
        
        elif operation_type == 'rotate':
            degrees = op.get('degrees', 0)  # Default rotation is 0 degrees
            image = RotateProcessor(image, degrees).process_image().get_image()
            
        elif operation_type == 'grayscale':
            image = GrayscaleProcessor(image).process_image().get_image()
            
        elif operation_type == 'resize':
            width = op['width']
            height = op['height']
            image = ResizeProcessor(image, width, height).process_image().get_image()
            
        elif operation_type == 'thumbnail':
            max_width = op['max_width']
            max_height = op['max_height']
            image = ThumbnailProcessor(image, max_width, max_height).process_image().get_image()
            
        elif operation_type == 'rotateLeft':
            image = RotateLeftProcessor(image).process_image().get_image()
            
        elif operation_type == 'rotateRight':
            image = RotateRightProcessor(image).process_image().get_image()
            

        
    # After processing, convert the image back to bytes
    _, buf = cv2.imencode('.jpg', image)
    return io.BytesIO(buf)
