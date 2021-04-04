from graia.saya import Saya, Channel
from graia.application.message.chain import MessageChain
from graia.application import GraiaMiraiApplication
from graia.application.group import Group
from graia.application.message.elements.internal import Plain
import click
from click.testing import CliRunner
from asyncio import tasks


@click.group()
def nian():
    pass


@click.argument('thing')
@click.command(name='echo')
def echo(thing:  str):
    print(thing)


@click.command(name='test')
def test():
    print(__file__)


nian.add_command(echo)
nian.add_command(test)


async def group_cli(app: GraiaMiraiApplication, msg: list, group: Group):
    runner = CliRunner()
    rest = runner.invoke(nian, msg)
    await app.sendGroupMessage(group,MessageChain.create([Plain(str(rest.output))]))

saya = Saya.current()
channel = Channel.current()
bcc = saya.broadcast


@bcc.receiver('GroupMessage')
# ,dispatchers=[Kanata([FullMatch('nian'),RequireParam('args')])])
async def cli_listener(app: GraiaMiraiApplication, ctx: MessageChain, group: Group):
    if ctx.asDisplay().startswith("nian "):
        msg = ctx.getFirst(Plain)
        msg_text = msg.text[5:]
        msg_list = msg_text.split(' ')
        task = tasks.create_task(group_cli(app, msg_list, group))
        await task
