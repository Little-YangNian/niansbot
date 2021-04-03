from .qwq import get_cli

from graia.application import GraiaMiraiApplication
from graia.application.event.messages import GroupMessage
from graia.application.group import Group
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, Image
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import imgkit as ik

saya = Saya.current()
channel = Channel.current()

async def g(url):
    cfg = ik.config(wkhtmltoimage="/usr/bin/wkhtmltoimage")
    await ik.from_url(url,'out.jpg',config=cfg)
@channel.use(ListenerSchema(
    listening_events=[GroupMessage]
))
async def friend_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    if message.has(Plain) and message.asDisplay().startswith("wti "):
        print("开始生成")
        m = message.getFirst(Plain).text[4:]
        try:
            await g(m)
        except:
            pass
        await app.sendGroupMessage(group,
                MessageChain.create(
                    [Image.fromLocalFile
                    ('out.jpg')]))
