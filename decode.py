import cv2
import json


class DecodeQrCode:
    def __init__(self, source):
        self.source = source
        self.qr_reader = cv2.QRCodeDetecto

