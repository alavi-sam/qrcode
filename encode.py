import qrcode
from PIL import Image


class EncodeQRCode:
    def __init__(self, path_name, data, box_size, border_size, fill_color, back_color):
        self.path_name = path_name
        self.data = data
        self.fill_color = fill_color
        self.back_color = back_color
        self.box_size =  box_size
        self.border_size = border_size
        self.qr_instance = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        self.img_qr = None
