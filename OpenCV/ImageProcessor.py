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
        return self

# Rotate Operation
class RotateProcessor(ImageProcessor):
    def __init__(self, image, angle):
        super().__init__(image)
        self.angle = angle
        
    def process_image(self):
        (h, w) = self.image.shape[:2]
        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, self.angle, 1.0)
        self.image = cv2.warpAffine(self.image, M, (w, h))
        return self

# Grayscale Operation
class GrayscaleProcessor(ImageProcessor):
    def __init__(self, image):
        super().__init__(image)
        
    def process_image(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return self

# Resize Operation
class ResizeProcessor(ImageProcessor):
    def __init__(self, image, width, height):
        super().__init__(image)
        self.width = width
        self.height = height
        
    def process_image(self):
        self.image = cv2.resize(self.image, (self.width, self.height))
        return self

# Thumbnail Operation (similar to Resize but with aspect ratio consideration)
class ThumbnailProcessor(ImageProcessor):
    def __init__(self, image, max_width, max_height):
        super().__init__(image)
        self.max_width = max_width
        self.max_height = max_height
        
    def process_image(self):
        h, w = self.image.shape[:2]
        scaling_factor = min(self.max_width / w, self.max_height / h)
        new_size = (int(w * scaling_factor), int(h * scaling_factor))
        self.image = cv2.resize(self.image, new_size)
        return self

# Rotate Left (90 degrees CCW)
class RotateLeftProcessor(ImageProcessor):
    def __init__(self, image):
        super().__init__(image)
        
    def process_image(self):
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return self

# Rotate Right (90 degrees CW)
class RotateRightProcessor(ImageProcessor):
    def __init__(self, image):
        super().__init__(image)
        
    def process_image(self):
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        return self
        
if __name__ == "__main__":
    image_path = "profile.jpg"
    image = cv2.imread(image_path)
    if image is None:
        print("Error loading image")
    else:
        print("Image loaded successfully")
        # Apply a sequence of processing steps
        processed_image = FlipProcessor(image, 1).process_image().get_image()
        processed_image = GrayscaleProcessor(processed_image).process_image().get_image()
        # You can continue chaining other processing operations as needed

        # Show the final result
        cv2.imshow('Processed Image', processed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()