from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour
from graia.application.message.elements.internal import Plain, Image
from graia.application.group import Group, Member
from tool.config import yaml_to_session
loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
saya = Saya(bcc)
saya.install_behaviours(BroadcastBehaviour(bcc))
with saya.module_context():
    saya.require("saya.cli")
    saya.require('saya.rua')
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=yaml_to_session()
)
app.launch_blocking()
