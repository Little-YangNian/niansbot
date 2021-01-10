from apps.app import bcc,app
from graia.application.message.chain import MessageChain
from graia.application.group import Group,Member
from graia.application.message.elements.internal import Plain,At,Image
from graia.application import GraiaMiraiApplication
from plugin.plugins.nb import NiuBi
from plugin.plugins.rua import ruaer
import re

@bcc.receiver('GroupMessage')
async def rua(app: GraiaMiraiApplication,member:Member,message:MessageChain,group:Group):
    if message.asDisplay().startswith('rua'):
    #output = await ruaer(member.id)
        b = message.get(At)
        if b :
        
            print(b[0])
            c = str(b[0])
            at_user = re.findall('target=.*?(.*?) display=',c)
            url =  ruaer(int(at_user[0]))
            print(url)
            await app.sendGroupMessage(group,MessageChain.create([Image.fromLocalFile(url)]))
@bcc.receiver("GroupMessage")
async def nb(app: GraiaMiraiApplication,group: Group,message: MessageChain):
    if message.asDisplay().startswith("nb"):
        at = message.get(At)
        if at:
            ats = at[0]
            at_user = re.findall("display='\@.*?(.*?)'",str(ats))
            rest = NiuBi(at_user[0])
            await app.sendGroupMessage(group,MessageChain.create([Plain(rest)]))
