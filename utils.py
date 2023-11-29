from encode import EncodeQRCode
import textwrap
from PIL import Image, ImageDraw, ImageFont
import os


def create_image(width, height, bgColor, text, text_size=10, alligned_width=10):
    import arabic_reshaper
    from bidi.algorithm import get_display
    # text = text.encode('utf-8')
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)     
    font = ImageFont.truetype('fonts\sahel.ttf', size=text_size, encoding='utf-8')
    alligned_text = textwrap.wrap(bidi_text, width=alligned_width)[::-1]
    img = Image.new(mode='RGB', size=(width, height), color=bgColor)
    draw = ImageDraw.Draw(img, mode='RGB')

    current_h, pad = 35 if len(alligned_text) == 1 else 20, 5
    for line in alligned_text:
        w, h = draw.textsize(line, font=font)
        draw.text(((width-w)/2, current_h), line, font=font, allign='center', fill=(0,0,0))
        current_h += h + pad
    return img


def create_from_csv(file_path):
    import pandas as pd
    df = pd.read_csv(file_path)
    os.makedirs('QRCodes', exist_ok=True)
    for idx, row in df.iterrows():
        data_dict = row.to_dict()
        qr_instance = EncodeQRCode(
            path_name=os.path.join('QRCodes', f'{data_dict["ProductCode"]}.jpg'),
            data = data_dict,   
        )
        qr_instance.create_qrcode()
        logo = create_image(width=100, height=100, bgColor=(255, 255, 255), text=data_dict['SKUName'])
        qr_instance.add_logo(logo, 100)
        qr_instance.save()
    




