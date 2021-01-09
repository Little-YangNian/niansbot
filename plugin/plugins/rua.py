import re
from io import BytesIO
from os import path
from PIL import Image
from resource.rua.data_source import generate_gif
import requests

data_dir = './resource/rua/data'
def ruaer(id):
    url = f'http://q1.qlogo.cn/g?b=qq&nk={id}&s=160'
    resp =  requests.get(url)
    resp_cont =  resp.content
    avatar = Image.open(BytesIO(resp_cont))
    output = generate_gif(data_dir, avatar)
    print(output)
    return output
