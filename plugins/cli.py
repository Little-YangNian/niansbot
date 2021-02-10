from graia.application import Member,MessageChain,Group,GraiaMiraiApplication
from graia.application.message.elements.internal import Plain
import subprocess
from miraibot import get
bcc = get.bcc()

@bcc.receiver("GroupMessage")
async def cli(mem:Member,app:GraiaMiraiApplication,group:Group,ctx:MessageChain):
    if ctx.asDisplay().startswith("nian "):
        res = subprocess.getoutput(f"python3 plugins/CLI.py {ctx.asDisplay()[5:]}")
        await app.sendGroupMessage(group,
                MessageChain.create(
                    [
                        Plain(
                            res
                            )
                        ]
                    )
                )
    elif ctx.asDisplay().startswith("sh ") and mem.id == 2544704967:
        res = subprocess.getoutput(ctx.asDisplay()[3:])
        await app.sendGroupMessage(
                group,
                MessageChain.create([
                    Plain(
                        res
                        )
                    ]
                )
            )

    else:
        pass

