from .qwq import get_cli

from graia.application import GraiaMiraiApplication
from graia.application.event.messages import GroupMessage
from graia.application.group import Group
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, Image
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(
    listening_events=[GroupMessage]
))
async def friend_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    if message.has(Plain) and message.asDisplay().startswith("nian "):
        m = message.getFirst(Plain).text[5:]
        resp = await get_cli(m.split(" "))
        if resp.output.startswith("IMGMSG:PATH="):
            path = resp.output.replace("IMGMSG:PATH=","")
            print(path)
            await app.sendGroupMessage(group, MessageChain.create(
                [Image.fromLocalFile(path)]))
        else:
            await app.sendGroupMessage(group,MessageChain.create(
                [Plain(resp.output)]))
