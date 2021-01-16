import re

from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, At, Image

from apps.app import bcc
from plugin.plugins.nb import NiuBi
from plugin.plugins.rua import ruaer
from plugin.plugins.status import sys_status
from  plugin.plugins.Key_talker import msger

@bcc.receiver('GroupMessage')
async def rua(app: GraiaMiraiApplication, member: Member, message: MessageChain, group: Group):
    if message.asDisplay().startswith('rua'):
        atmsg = message.get(At)
        if atmsg:
            atmsger = str(atmsg[0])
            at_user = re.findall('target=.*?(.*?) display=', atmsger)
            url = ruaer(int(at_user[0]))
            print(url)
            await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile(url)]))


@bcc.receiver("GroupMessage")
async def nb(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    if message.asDisplay().startswith("nb"):
        at = message.get(At)
        if at:
            ats = at[0]
            at_user = re.findall("display='\@.*?(.*?)'", str(ats))
            rest = NiuBi(at_user[0])
            await app.sendGroupMessage(group, MessageChain.create([Plain(rest)]))
    else:
        pass


@bcc.receiver("GroupMessage")
async def get_status(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    if message.asDisplay() == 'BOTSTATUS' or message.asDisplay() == '机器人状态':
        rest = sys_status()
        await app.sendGroupMessage(group, MessageChain.create([Plain(rest)]))
    else:
        pass

@bcc.receiver("GroupMessage")
async def talker(app: GraiaMiraiApplication, group: Group, message: MessageChain,member: Member):
    rest = msger(message.asDisplay(),member.id)
    if rest != None:
        await app.sendGroupMessage(group,MessageChain.create([Plain(rest)]))
    else:
        pass