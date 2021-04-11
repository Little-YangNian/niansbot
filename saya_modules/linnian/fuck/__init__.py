import ujson
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import random
from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import  At, Image, Plain
from graia.application.event.messages import GroupMessage
from graia.application.message.chain import MessageChain
from graia.application.group import Group, Member
import aiofiles
saya = Saya.current()
channel = Channel.current()

data_path = "./saya_modules/linnian/fuck/data.json"

@channel.use(ListenerSchema(
    listening_events=[GroupMessage]
))
async def rua(app: GraiaMiraiApplication,member: Member
        ,group: Group,msg: MessageChain):
    if msg.has(At) and msg.getFirst(At).target == 1063247201:
        m = msg.getFirst(Plain).text
        async with aiofiles.open(data_path,encoding="utf-8") as f:
            f = await f.read()
            lib = ujson.loads(f)
            try:
                reply = lib[m]
                chain = MessageChain.create([At(member.id),Plain(random.choice(reply))])
                await app.sendGroupMessage(group,chain)
            except:
                pass
