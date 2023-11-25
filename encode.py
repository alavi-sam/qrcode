import json
from sys import version
import qrcode
from PIL import Image
import argparse


class EncodeQRCode:
    def __init__(self, path_name, data, box_size, border_size, fill_color, back_color):
        self.path_name = path_name
        self.data = data
        self.fill_color = fill_color
        self.back_color = back_color
        self.box_size =  box_size
        self.border_size = border_size
        self.qr_instance = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            version=1
        )
        self.img_qr = None

    def create_qrcode(self):
        self.qr_instance.add_data(self.data)
        self.qr_instance.make(fit=True)
        self.img_qr = self.qr_instance.make_image(fill_color=self.fill_color, back_color=self.back_color)

    def add_logo(self, logo_path, logo_size):
        logo_img = Image.open(logo_path)
        logo_img.thumbnail(size=(logo_size, logo_size))
        logo_position = ((self.img_qr.size[0] - logo_size)//2, (self.img_qr.size[1] - logo_size)//2)
        self.img_qr.paste(logo_img, logo_position)

    def save(self):
        self.img_qr.save(self.path_name)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='CLI commands for creating QR Code from user inputs')

    parser.add_argument('--path', type=str, required=True, help='Enter a path for you QR Code to be saved.')
    parser.add_argument('--data-item', action='append', required=True, help='Enter your QR Code data')
    parser.add_argument('--box-size', type=int, required=False, help='QR Code box size')
    parser.add_argument('--border-size', type=int, required=False, help='QR Code border size')
    parser.add_argument('--fill-color', type=tuple, required=False, help='Pass a tuple containing RGB values for your QR Code content color')
    parser.add_argument('--back-color', type=tuple, required=False, help='Pass a tuple containing RGB values for your QR Code backgrond color')
    parser.add_argument('--logo-path', type=str, required=False, help='If you want to have a logo in your QR Code pass the logo path')
    parser.add_argument('--logo-size', type=int, required=False, help='Input logo size the more little the logo the better QR Code')

    args = parser.parse_args()


    if not args.logo_path and args.logo_size:
        parser.error('--logo-path is required when --logo-size in provided!')

    data = dict(item.split('=') for item in args.data_item)

    fill_color = args.fill_color if args.fill_color else 'black'
    back_color = args.back_color if args.back_color else 'white'

    if isinstance(fill_color, tuple):
        fill_hex = '#{:02x}{:02x}{:02x}'.format(*fill_color)
    if isinstance(back_color, tuple):
        back_hex = '#{:02x}{:02x}{:02x}'.format(*back_color)

    qr = EncodeQRCode(
        path_name=args.path,
        data=data,
        box_size=args.box_size if args.box_size else 100,
        border_size=args.border_size if args.border_size else 20,
        fill_color=fill_color,
        back_color=back_color
    )

    qr.create_qrcode()

    if args.logo_path:
        qr.add_logo(args.logo_path, logo_size=args.logo_size if args.logo_size else 100)

    qr.save()
