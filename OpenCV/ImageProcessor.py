import cv2
from abc import ABC, abstractmethod

class ImageProcessor(ABC):
    def __init__(self, image):
        self.image = image
        
    @abstractmethod
    def process_image(self):
        pass
    
    def show_image(self):
        cv2.imshow('Image', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def get_image(self):
        return self.image
    

class FlipProcessor(ImageProcessor):
    def __init__(self, image, flip_code):
        super().__init__(image)
        self.flip_code = flip_code  # 0 for vertical, 1 for horizontal, -1 for both
        
    def process_image(self):
        self.image = cv2.flip(self.image, self.flip_code)
        
        print(f"Flipped image in {self.flip_code} direction")
        return self

# Rotate Operation
class RotateProcessor(ImageProcessor):
    def __init__(self, image, angle):
        super().__init__(image)
        # Ensure angle is an integer, rounding if necessary. This ensures that
        # at least it doesn't fail and some image is returned
        self.angle = round(angle)
        
    def process_image(self):
        (h, w) = self.image.shape[:2]
        center = (w / 2, h / 2)
        # Adjust angle for clockwise rotation if desired
        # - is counter-clockwise, + is clockwise
        M = cv2.getRotationMatrix2D(center, -self.angle, 1.0)  # Note the '-' sign to adjust direction
        self.image = cv2.warpAffine(self.image, M, (w, h))
        
        print(f"Rotated by {self.angle} degrees")
        return self

# Grayscale Operation
class GrayscaleProcessor(ImageProcessor):
    def __init__(self, image):
        super().__init__(image)
        
    def process_image(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        print("Converted to grayscale")
        return self

# Resize Operation
class ResizeProcessor(ImageProcessor):
    def __init__(self, image, percentage):
        super().__init__(image)
        self.percentage = percentage

    def process_image(self):
        # Calculate new dimensions
        width = int(self.image.shape[1] * self.percentage / 100)
        height = int(self.image.shape[0] * self.percentage / 100)

        # Resize the image
        self.image = cv2.resize(self.image, (width, height))

        print(f"Resized to {width}x{height} ({self.percentage}%)")
        return self
    
    
# Thumbnail Operation (similar to Resize but with aspect ratio consideration)
class ThumbnailProcessor(ImageProcessor):
    def __init__(self, image, max_width=200, max_height=200):
        super().__init__(image)
        self.max_width = max_width
        self.max_height = max_height
        
    def process_image(self):
        # Calculate the scaling factor to preserve aspect ratio
        h, w = self.image.shape[:2]
        scaling_factor = min(self.max_width / w, self.max_height / h)
        new_size = (int(w * scaling_factor), int(h * scaling_factor))

        # Resize the image with aspect ratio preservation
        self.image = cv2.resize(self.image, new_size)

        # Calculate padding for letter-boxing
        delta_w = self.max_width - new_size[0]
        delta_h = self.max_height - new_size[1]
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)

        # Add padding to the image to achieve the thumbnail size with letter-boxing
        color = [0, 0, 0]  # Black padding
        self.image = cv2.copyMakeBorder(self.image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        
        # Log that thumbnail is created
        print("Thumbnail created")
        
        return self

# Rotate Left (90 degrees CCW)
class RotateLeftProcessor(ImageProcessor):
    def __init__(self, image):
        super().__init__(image)
        
    def process_image(self):
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        print("Rotated left")
        return self

# Rotate Right (90 degrees CW)
class RotateRightProcessor(ImageProcessor):
    def __init__(self, image):
        super().__init__(image)
        
    def process_image(self):
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        print("Rotated right")
        return self
        