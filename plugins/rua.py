import re
from io import BytesIO
from os import path
from PIL import Image as im
from .rua_data.data_source import generate_gif
import aiohttp
from miraibot import get,GraiaMiraiApplication
from miraibot.message import Image,Member,At,Group,MessageChain
import os

data_dir = os.path.join(path.dirname(__file__), 'rua_data/data')
async def ruaer(id):
    url = f'http://q1.qlogo.cn/g?b=qq&nk={id}&s=160'
    async with aiohttp.request("get",url) as resp:
        resp_cont = await resp.read()
    avatar = im.open(BytesIO(resp_cont))
    output = generate_gif(data_dir, avatar)
    return output

bcc = get.bcc()

@bcc.receiver("GroupMessage")
async def rua(app: GraiaMiraiApplication,member: Member
        ,group: Group,msg: MessageChain):
    if msg.asDisplay().startswith("rua"):

            qid = msg.get(At)[0].target
            url = await ruaer(qid)
            ph = Image.fromLocalFile(url)
            await app.sendGroupMessage(group,
                    MessageChain.create(
                        [ph])
                    )

    else:
        pass


