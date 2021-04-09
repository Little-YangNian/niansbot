import yaml
from graia.application import GraiaMiraiApplication
from graia.application.event.messages import GroupMessage, FriendMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, Image
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import aiofiles
from graia.application.friend import Friend


config_path = "./config/comment.yml"
admin = 2544704967

saya = Saya.current()
channel = Channel.current()

@channel.use(ListenerSchema(
    listening_events=[GroupMessage]
))
async def friend_message_listener(app: GraiaMiraiApplication, group: Group, ctx: MessageChain,member: Member):
    if  ctx.asDisplay() == "#在此群订阅评论" and member.id == admin:
        async with aiofiles.open(config_path,encoding="utf-8",mode="a+") as f:
            await f.write(f"{group.id}: true")
            await app.sendGroupMessage(group
                    ,MessageChain.create(
                        [Plain("成功")]))
    elif ctx.asDisplay() == "#停止评论订阅" and member.id == admin:
        async with aiofiles.open(config_path,mode="r",encoding="utf-8") as f:
            yml = yaml.load(await f.read(),Loader=yaml.SafeLoader)
            del yml[group.id]
            dumps = yaml.dump(yml,Dumper=yaml.SafeDumper)
        async with aiofiles.open(config_path,mode="w",encoding="utf-8") as f:
            await f.write(dumps)
            await app.sendGroupMessage(group,
                MessageChain.create(
                    [Plain("成功")]))

@channel.use(ListenerSchema(
    listening_events=[FriendMessage]))
async def qmsg(app: GraiaMiraiApplication,friend: Friend,ctx: MessageChain):
    if friend.id == 3579038285 and ctx.asDisplay().startswith("霖念の小站有新评论了"):
        m = ctx.asDisplay()
        ip = m.find(r"评论人IP")
        content = m.find("评论内容")
        resp = m[:ip+6] + "\n" + m[content:]
        async with aiofiles.open(config_path,encoding="utf-8") as f:
            yml = yaml.load(await f.read(),Loader=yaml.SafeLoader)
            for i in yml.keys():
                await app.sendGroupMessage(int(i),
                        MessageChain.create([Plain(resp)]))

