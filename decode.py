import cv2
import json
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np



class Decode:
    def __init__(self, image):
        self.image = image


    def detect(self):
        if isinstance(self.image, np.ndarray) or isinstance(self.image, Image):
            res = decode(self.image)
        elif isinstance(self.image, str):
            image = Image.open(self.image)
            res = decode(image)
        else:
            raise TypeError(f'wrong image input with type ({type(self.image)}). You should input either str, np array, or PIL Image')
        
        result_dicts = [{
            'data': qr.data.decode('utf-8'),
            'boundingBox': {
                'x': qr.rect.left,
                'y': qr.rect.top,
                'width': qr.rect.width,
                'height': qr.rect.height
            },
            'orientation': qr.orientation
        } for qr in res]

        return result_dicts 



