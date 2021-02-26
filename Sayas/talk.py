import yaml
from graia.application import GraiaMiraiApplication
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, At
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import aiofiles
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter

saya = Saya.current()
channel = Channel.current()
bcc = saya.broadcast
inc = InterruptControl(bcc)

admin = [2544704967]

global chat
chat = {}


@channel.use(ListenerSchema(
    listening_events=[GroupMessage]
))
async def talk(app: GraiaMiraiApplication, group: Group, member: Member, ctx: MessageChain):
    if ctx.asDisplay().startswith("调教 "):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain("发送调教内容(回复内容)")
        ]))

        @Waiter.create_using_function([GroupMessage])
        async def waiter(
                event: GroupMessage, waiter_group: Group,
                waiter_member: Member, waiter_message: MessageChain
        ):
            if all([
                waiter_group.id == group.id,
                waiter_member.id == member.id
            ]):
                key = ctx.asDisplay()[3:]
                value = waiter_message.asDisplay()
                await add(key, value)
                load()
                return event

        await inc.wait(waiter)
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("执行完毕.")
        ]))
    if ctx.asDisplay().startswith('移除 '):
        await remove(ctx.asDisplay()[3:])
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("执行完毕.")
        ]))
    try:
        await app.sendGroupMessage(group, MessageChain.create(
        [Plain(chat[ctx.asDisplay()])]
    ))
    except KeyError:
        pass


def load():
    with open('talk.yml',encoding='utf-8') as f:
        t = f.read()
        f_dict = yaml.load(t, Loader=yaml.SafeLoader)
        for k, v in f_dict.items():
            chat[k] = v


async def add(key, value):
    async with aiofiles.open('talk.yml', mode='a', encoding='utf-8') as f:
        await f.write(f'\n"{key}": "{value}"\n')

async def remove(key):
    del chat[key]
    f = yaml.dump(chat,Dumper=yaml.SafeDumper)
    async with aiofiles.open('talk.yml', mode='w', encoding='utf-8') as a:
        await a.write(f)

load()
