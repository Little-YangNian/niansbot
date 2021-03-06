from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication
import asyncio
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour
from tools.mah import mah_config
loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
saya = Saya(bcc)
saya.install_behaviours(BroadcastBehaviour(bcc))
with saya.module_context():
    saya.require("saya_modules.linnian.rua")
    saya.require("saya_modules.linnian.fuck")
    saya.require("saya_modules.kawaii.SteamGameSearcher")
    saya.require("saya_modules.kawaii.NetworkCompiler")
    # saya.require('saya.rua')
    saya.require("saya_modules.kawaii.GroupWordCloudGenerator")
#    saya.require("modules.GithubHotSearch")


app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=mah_config('mah.yml')
)
app.launch_blocking()
