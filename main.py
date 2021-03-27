from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour
from graia.application.message.elements.internal import Plain, Image
from graia.application.group import Group, Member

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
saya = Saya(bcc)
saya.install_behaviours(BroadcastBehaviour(bcc))

app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",  # 填入 httpapi 服务运行的地址
        authKey="qaq1940QAQ",  # 填入 authKey
        account=1063247201,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

with saya.module_context():
    saya.require("Sayas.nbnhhsh")
    saya.require('Sayas.talk')
    saya.require('Sayas.rua')
    saya.require('Sayas.baidu')


@bcc.receiver("GroupMessage")
async def friend_message_listener(app: GraiaMiraiApplication, member: Member, msg: MessageChain, group: Group):
    if msg.has(Image):
        photos = msg.get(Image)
        for i in photos:
            print(f"[Photo] {member.id} Send a Photo\nurl is {i.url}")
    if msg.asDisplay() == '#Test':
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("Hello, World!")
        ]))
    if msg.asDisplay().startswith("复读 "):
        await app.sendGroupMessage(group, MessageChain.create([Plain(msg.asDisplay()[3:])]))
    if msg.asDisplay().startswith("#debug ") and member.id == 2544704967:
        if "# Chain" in  msg.asDisplay():
            await app.sendGroupMessage(group,MessageChain.create([Plain(str(msg))]))
        code = msg.asDisplay()[7:]
        await app.sendGroupMessage(group,MessageChain.create([Plain(str(eval(code)))]))
app.launch_blocking()
