import imgkit
import click
from click.testing import CliRunner
from click.testing import Result
from graia.application.message.chain import MessageChain as Msg
from graia.application.message.elements.internal import Plain,Image


@click.group()
def nian():
    pass
@click.argument('echo')
@click.command(name='echo')
def echo(echo):
    print(echo)    
@click.command(name='owo')
def owo():
    print("qwq")
@click.argument("url")
@click.command(name="web",help="传入网址生成图片")
def web(url: str):
    cfg = imgkit.config(wkhtmltoimage="/usr/bin/wkhtmltoimage")
    imgkit.from_url(url=url,output_path="out.png",config=cfg)
    print(f"IMGMSG:PATH=./out.png")
nian.add_command(echo)
nian.add_command(owo)
nian.add_command(web)
# a = qwq(['xwx']).invoke(

ts = CliRunner()

async def get_cli(cmd_list: list)-> Result:
    rest = ts.invoke(nian,args=cmd_list)
    return rest
