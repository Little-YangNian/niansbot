import aiohttp
from miraibot import get
from miraibot import GraiaMiraiApplication
from miraibot.message import MessageChain, Group, Member
import json

commands  =  ['ft','在吗']
groups = [12345678]
hosts = {}
# Group:Host

bcc = get.bcc()


@bcc.receiver('GroupMessage')
async def mc_tool(msg: MessageChain, group: Group, member: Member,app: GraiaMiraiApplication):
    ctx = msg.asDisplay()
    if ctx in commands and group.id in groups:
        
        async with aiohttp.request('get',f'https://api.bluesdawn.top/minecraft/server/api?host={hosts[group.id]}') as rest:
            respon  = await rest.text()
        
