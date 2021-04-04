from io import BytesIO
from os import path
from PIL import Image as im
from saya.rua_data.data_source import generate_gif
import aiohttp

import os
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import  At, Image
from graia.application.event.messages import GroupMessage
from graia.application.message.chain import MessageChain
from graia.application.group import Group, Member

saya = Saya.current()
channel = Channel.current()



data_dir = os.path.join(path.dirname(__file__), 'rua_data/data')
async def ruaer(id):
    url = f'http://q1.qlogo.cn/g?b=qq&nk={id}&s=160'
    async with aiohttp.request("get",url) as resp:
        resp_cont = await resp.read()
    avatar = im.open(BytesIO(resp_cont))
    output = generate_gif(data_dir, avatar)
    return output


@channel.use(ListenerSchema(
    listening_events=[GroupMessage]
))
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


