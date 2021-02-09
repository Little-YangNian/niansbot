import aiohttp
import aiofiles
from miraibot import get
from miraibot import GraiaMiraiApplication
from miraibot.message import MessageChain, Image,  Group, Member, Plain
import json
import base64
import os

commands  =  ['ft','在吗']
groups = [488467276]

host = "cn-xz-bgp.sakurafrp.com:23300"

bcc = get.bcc()


@bcc.receiver('GroupMessage')
async def mc_tool(msg: MessageChain, group: Group, member: Member,app: GraiaMiraiApplication):
    ctx = msg.asDisplay()
    if ctx in commands and group.id in groups:
        
        async with aiohttp.request('get',f'https://api.bluesdawn.top/minecraft/server/api?host={host}') as rest:
            respon  = await rest.read()
            res = json.loads(respon)
            code = res["favicon"]
            player = ""
            favicon = base64.b64decode((code.replace(r"data:image/png;base64,","")))
            for i in res['players']['list']:
                player = player + i['name'] + '\n'
            async with aiofiles.open("fav.png",mode="wb") as f:
                await f.write(favicon)
            result = f"服务器查询:\n状态:{res['status']}\n{res['version']['version']}\n在线玩家:{player}\n"
            chain = msg.create(
                    [Plain(result),Image.fromLocalFile("./fav.png")]
                    )
            await app.sendGroupMessage(group,chain)
        
