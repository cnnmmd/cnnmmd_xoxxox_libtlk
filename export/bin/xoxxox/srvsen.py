import json
import importlib.util
import argparse
from aiohttp import web
from xoxxox.params import Config, Engine
from xoxxox.shared import Custom

#---------------------------------------------------------------------------

def getprc(engine):
  s = importlib.util.spec_from_file_location("module", f"{Engine.dirprc}/{engine}.py")
  module = importlib.util.module_from_spec(s)
  s.loader.exec_module(module)
  return module

async def ressys(datreq):
  dicreq = await datreq.json()
  senprc.status(**dicreq)
  return web.Response(
    text=json.dumps({"return": "1"}),
    content_type="application/json",
  )

async def resgen(datreq):
  dicreq = await datreq.json()
  txtreq = dicreq["txtreq"]
  txtres = senprc.infere(txtreq)
  return web.Response(
    text=json.dumps({"txtres": txtres}),
    content_type="application/json",
  )

#---------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--secure", default="0")
parser.add_argument("--svport", type=int, default="80")
parser.add_argument("--engine", default="luk")
parser.add_argument("--gensyn", default="1")
parser.add_argument("--config")
parser.add_argument("--adraco", type=str) # default: cnfnet
parser.add_argument("--pthcrt", type=str) # default: cnfnet
parser.add_argument("--pthkey", type=str) # default: cnfnet
objarg = parser.parse_args()

dicnet = Custom.update(Config.cnfnet, {k: v for k, v in vars(objarg).items() if v is not None})
dicprm = {k: v for k, v in vars(objarg).items() if v is not None}

dicprm.pop("secure")
dicprm.pop("svport")
dicprm.pop("engine")
dicprm.pop("gensyn")
secure = objarg.secure
svport = objarg.svport
engine = objarg.engine
gensyn = objarg.gensyn

adrsys = "/sys"
adrgen = "/gen"

#---------------------------------------------------------------------------

module = getprc(engine)
senprc = module.SenPrc(**dicprm)
appweb = web.Application()
appweb.add_routes([web.post(adrsys, ressys)])
appweb.add_routes([web.post(adrgen, resgen)])
if secure == "0":
  web.run_app(appweb, port=svport)
if secure == "1":
  import ssl
  sslcon = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  sslcon.load_cert_chain(dicnet["pthcrt"], dicnet["pthkey"])
  web.run_app(appweb, port=svport, ssl_context=sslcon)
