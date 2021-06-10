import sys
import os
import json
import math
import qrcode
import numpy as np
import base64
from PIL import Image
from io import BytesIO
from src.elastic_search import ElasticSearchUtils

class QRGenerator:
    
    def __init__(self, json_data, index='test-index'):
        self.data = json_data
        self.split_parts = 4
        elastic = ElasticSearchUtils()
        elastic.ingest_data(data=self.data, index=index)
    
    def data_spliter(self):
        data_len = len(self.data)
        data_parts = [dict() for x in range(self.split_parts)]
        multiplier = math.gcd(self.split_parts, data_len)*self.split_parts
        for j in range(multiplier):
            if j%2 == 0:
                for i, (key, value) in enumerate(self.data.items()):
                    my_dict = data_parts[i%self.split_parts]
                    my_dict[key]=value
                    data_parts[i%self.split_parts] = my_dict
            else:
                for i, (key, value) in enumerate(reversed(self.data.items())):
                    my_dict = data_parts[i%self.split_parts]
                    my_dict[key]=value
                    data_parts[i%self.split_parts] = my_dict
        return data_parts
    
    @staticmethod
    def get_qr_image(data):
        qr = qrcode.QRCode(
            version=1, 
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10, 
            border=1)
        qr.add_data(data)
        qr.make(fit=True)
        print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
        img = qr.make_image(fill_color="white", back_color="black")
        img = img.resize((500,500))
        return img

    def make_qr(self, index='test-index'):
        data_parts = self.data_spliter()
        qrs = list()
        for data in data_parts:
            qrs.append(self.get_qr_image(data))
        return self.combine_qr(qrs)

    @staticmethod
    def combine_qr(images):
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)//2
        max_height = sum(heights)//2

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        y_offset = 0
        new_im.paste(images[0], (x_offset,y_offset))
        x_offset += images[0].size[0]
        new_im.paste(images[1], (x_offset,y_offset))
        y_offset += images[1].size[1]
        new_im.paste(images[2], (0,y_offset))
        new_im.paste(images[3], (x_offset,y_offset))
        buffered = BytesIO()
        new_im.save(buffered, format="JPEG")
        new_im.save('test.jpeg')
        return base64.b64encode(buffered.getvalue())
        

# if __name__ == '__main__':
#     data_path = os.path.join('.','src','test.json')
#     print(data_path)
#     with open(data_path) as json_file:
#         data = json.load(json_file)
#     ob = QRGenerator(data, 'testing123') 
#     print(ob.make_qr())