from graia.saya import Saya, Channel
from graia.application.message.chain import MessageChain
from graia.application import GraiaMiraiApplication
from graia.application.group import Group
from graia.application.message.elements.internal import Plain
import click
from click.testing import CliRunner
from asyncio import tasks
import httpx
import json
from .rss_lib import Rss

@click.group()
def nian():
    pass


@click.argument('thing')
@click.command(name='echo',help='把你输进去的什么jb东西又给吐出来')
def echo(thing:  str):
    print(thing)


@click.command(name='test')
def test():
    print(__file__)

@click.command(name='nbnhhsh',help='能不能好好说话缩写查询')
@click.argument('text')
def nbnhhsh(text: str):
    trans = ''
    tran = ''
    resp =  httpx.request("POST",'https://lab.magiconch.com/api/nbnhhsh/guess',json={'text': str(text)})
    try:
        trans = json.loads(resp.read())[0]['trans']
    except KeyError as e:
        print('可能暂时没有这个缩写！')
    for i in trans:
        if len(trans) == 1:
            tran = i
            break
        else:
            tran = tran + ' ' + i
    print(tran)

@click.command(name='rss',help='快速解析Rss和最新一篇博文')
@click.argument('url')
def rss(url: str):
    try:
        resp = Rss(url)
        feed = resp.get_feed()
        entire = resp.get_entries()
        result = f'Rss解析结果\n{feed.title}\n{feed.subtitle}\n最新博文:\n{entire.title}\n{entire.id}\n{entire.published}\n{entire.summary}'
        print(result)
    except Exception as e:
        print(e)


nian.add_command(echo)
nian.add_command(test)
nian.add_command(nbnhhsh)
nian.add_command(rss)



async def group_cli(app: GraiaMiraiApplication, msg: list, group: Group):
    runner = CliRunner()
    rest= runner.invoke(nian, msg)
    print(rest.output)
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
