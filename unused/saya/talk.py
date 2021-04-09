from graia.application import GraiaMiraiApplication
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, At
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter
from linnian.apps.chatter import Chater
from linnian.apps.chatter.tool import Tool

saya = Saya.current()
channel = Channel.current()
bcc = saya.broadcast
inc = InterruptControl(bcc)



@channel.use(ListenerSchema(
    listening_events=[GroupMessage]
))
async def talk(app: GraiaMiraiApplication, group: Group, member: Member, ctx: MessageChain):
    chat = Chater()
    if ctx.asDisplay().startswith("设置 "):
        await app.sendGroupMessage(group,MessageChain.create([Plain("发送回复内容w，必须是文字否则小霖念不会理你")]))
        @Waiter.create_using_function([GroupMessage])
        async def waiter(
                event: GroupMessage, waiter_group: Group,
                waiter_member: Member, waiter_message: MessageChain
        ):
            if all([
                waiter_group.id == group.id,
                waiter_member.id == member.id
            ]):
                if waiter_message.has(Plain):
                    key = ctx.getFirst(Plain).text[3:]
                    value = waiter_message.getFirst(Plain).text
                    mirai_code = False
                    if value.startswith("MiraiCode:"):
                        value = value[10:]
                        mirai_code = True
                    await chat.set(Tool.createKey(key,group.id),Tool.createReply(value,member.id,mirai_code))
                    await app.sendGroupMessage(group,MessageChain.create([Plain("成功啦Owo")]))
                    return event
                else:
                    await app.sendGroupMessage(group,
                            MessageChain.create([Plain("得是文字哦Xwx")]))

        await inc.wait(waiter)

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def get(app: GraiaMiraiApplication,msg: MessageChain,group: Group):
    chat = Chater()
    if msg.has(Plain):
        key = msg.getFirst(Plain).text
        resp = await chat.get_reply(Tool.createKey(key,group.id))
        if resp is None:
            pass
        else:
            mc = resp.mirai_code
            if mc:
                chain = MessageChain.fromSerializationString(resp.reply)
            else:
                chain = MessageChain.create([Plain(resp.reply)])
            await app.sendGroupMessage(group,chain)

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def remove(app: GraiaMiraiApplication,msg: MessageChain,group: Group):
    if msg.asDisplay().startswith("移除 "):
        main = msg.getFirst(Plain).text[3:]
        key = Tool.createKey(main,group.id)
        chat = Chater()
        try:
            resp = await chat.remove(key)
            await app.sendGroupMessage(group,MessageChain.create(
                [Plain(f"移除了{resp}个Key")]))
        except:
            pass
