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
  ttsprc.status(**dicreq)
  return web.Response(
    text=json.dumps({"return": "1"}),
    headers={
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': dicnet["adraco"]
    }
  )

async def resgen(datreq):
  dicreq = await datreq.json()
  txtreq = dicreq["txtreq"]
  if gensyn == "1":
    datwav = ttsprc.infere(txtreq)
  else:
    datwav = await ttsprc.infere(txtreq)
  datres = web.StreamResponse(
    status=200,
    reason="OK",
    headers={
      'Content-Type': 'audio/wav',
      'Content-Disposition': 'attachment; filename="output.wav"',
      'Access-Control-Allow-Origin': dicnet["adraco"]
    }
  )
  await datres.prepare(datreq)
  await datres.write(datwav)
  await datres.write_eof()
  return datres

# 追補（sys + gen ）
async def ressgn(datreq):
  global spkold
  dicreq = await datreq.json()
  skpnew = dicreq["keyspk"]
  if spkold != skpnew:
    ttsprc.status(**dicreq)
    spkold = skpnew
  txtreq = dicreq["txtreq"]
  datwav = ttsprc.infere(txtreq)
  datres = web.StreamResponse(
    status=200,
    reason="OK",
    headers={
      'Content-Type': 'audio/wav',
      'Content-Disposition': 'attachment; filename="output.wav"',
      'Access-Control-Allow-Origin': dicnet["adraco"]
    }
  )
  await datres.prepare(datreq)
  await datres.write(datwav)
  await datres.write_eof()
  return datres

async def optpst(datreq):
  return web.Response(
    headers={
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Origin': dicnet["adraco"]
    }
  )
  
#---------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--secure", default="0")
parser.add_argument("--svport", type=int, default="80")
parser.add_argument("--engine", default="xoxxox/ttsprc_ply")
parser.add_argument("--device", default="cpu")
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
adrsgn = "/sgn" # 追補（sys + gen ）

#---------------------------------------------------------------------------

spkold = "" # 追補（sys + gen ）
module = getprc(engine)
ttsprc = module.TtsPrc(**dicprm)
appweb = web.Application()
appweb.add_routes([web.post(adrgen, resgen)])
appweb.add_routes([web.post(adrsys, ressys)])
appweb.add_routes([web.post(adrsgn, ressgn)]) # 追補（sys + gen ）
appweb.add_routes([web.options(adrgen, optpst)])
appweb.add_routes([web.options(adrsys, optpst)])
appweb.add_routes([web.options(adrsgn, optpst)]) # 追補（sys + gen ）
if secure == "0":
  web.run_app(appweb, port=svport)
if secure == "1":
  import ssl
  sslcon = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  sslcon.load_cert_chain(dicnet["pthcrt"], dicnet["pthkey"])
  web.run_app(appweb, port=svport, ssl_context=sslcon)
