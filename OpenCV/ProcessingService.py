import numpy as np
import cv2
import io
from imghdr import what
from datetime import datetime  # For generating unique filenames

# Import your image processing classes
from .ImageProcessor import FlipProcessor, RotateProcessor, GrayscaleProcessor, ResizeProcessor, ThumbnailProcessor, RotateLeftProcessor, RotateRightProcessor

def convert_direction_to_code(direction):
    if direction == 'horizontal':
        return 1
    elif direction == 'vertical':
        return 0
    else:
        raise ValueError("Invalid flip direction. Must be 'horizontal' or 'vertical'.")
    
def validate_resize_percentage(percentage):
    if not -95 <= percentage <= 500:
        raise ValueError("Resize percentage must be between -95% and +500%.")

def validate_rotation_degrees(degrees):
    if not -10000 <= degrees <= 10000:
        raise ValueError("Rotation degrees must be between -10000 and +10000.")

def process_image_sequence(image_bytes, operations):
    print("Reached the ProcessingService.py")
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    processed_images = []  # This will store tuples of (filename, image_bytes)
    
    # Determine the image format and set it to jpg if it's not recognized
    image_format = what(io.BytesIO(image_bytes)) or 'jpg'
    
    # Process the image with the sequence of operations
    for i, op in enumerate(operations):
        operation_type = op['operation']
        
        if operation_type == 'flip':
            direction = op.get('direction', 'horizontal')  # Default to horizontal if not specified
            flip_code = convert_direction_to_code(direction)
            image = FlipProcessor(image, flip_code).process_image().get_image()
        
        elif operation_type == 'rotate':
            degrees = op.get('degrees', 0)  # Default rotation is 0 degrees
            validate_rotation_degrees(degrees)
            image = RotateProcessor(image, degrees).process_image().get_image()
            
        elif operation_type == 'grayscale':
            image = GrayscaleProcessor(image).process_image().get_image()
            
        elif operation_type == 'resize':
        
            percentage = op.get('percentage', 100)
            validate_resize_percentage(percentage)
            processor = ResizeProcessor(image, percentage)
            image = processor.process_image().get_image()
            
        elif operation_type == 'thumbnail':
            thumbnail_processor = ThumbnailProcessor(image)
            thumbnail_image = thumbnail_processor.process_image().get_image()
            
            # Convert thumbnail to bytes and store
            _, thumb_buf = cv2.imencode(f'.{image_format}', thumbnail_image)
            thumbnail_bytes = io.BytesIO(thumb_buf).getvalue()
            thumbnails_filename = f"thumbnail_{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{i}.{image_format}"
            processed_images.append((thumbnails_filename, thumbnail_bytes))
        
        elif operation_type == 'rotateLeft':
            image = RotateLeftProcessor(image).process_image().get_image()
        
        elif operation_type == 'rotateRight':
            image = RotateRightProcessor(image).process_image().get_image()
        else:
            raise ValueError(f"Invalid operation type: {operation_type}")

    # Convert the final processed image back to bytes
    _, final_buf = cv2.imencode(f'.{image_format}', image)
    final_image_bytes = io.BytesIO(final_buf).getvalue()
    
    # Store the final processed image with datetime in this format: final_processed_image_YYYY_MM_DD_HH:MM:SS.{image_format}
    final_filename = f"final_processed_image_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.{image_format}"
    processed_images.insert(0, (final_filename, final_image_bytes))  # Ensure the final image is the first in the list

    return processed_images
