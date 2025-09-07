import argparse
import asyncio
import aiohttp

#---------------------------------------------------------------------------

async def reqsys(dicreq, adrreq):
  async with aiohttp.ClientSession() as sssweb:
    async with sssweb.post(adrreq, json=dicreq) as datres:
      dicres = await datres.json()

async def reqgen(dicreq, adrreq):
  async with aiohttp.ClientSession() as sssweb:
    async with sssweb.post(adrreq, json=dicreq) as datres:
      dicres = await datres.json()
      return dicres

#---------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--server", default="http://localhost")
parser.add_argument("--config")
parser.add_argument("--prmmax", type=int)
parser.add_argument("--status")
parser.add_argument("--rolslf")
parser.add_argument("--roloth")
parser.add_argument("--inislf")
parser.add_argument("--inioth")
objarg = parser.parse_args()
dicprm = {k: v for k, v in vars(objarg).items() if v is not None}

dicprm.pop("server")
server = objarg.server

adssys = "/sys"
adsgen = "/gen"

#---------------------------------------------------------------------------

dicres = asyncio.run(reqsys(dicprm, server + adssys))
while True:
  print("> ", end="")
  dicprm["txtreq"] = input()
  dicres = asyncio.run(reqgen(dicprm, server + adsgen))
  print("< ", end="")
  print(dicres["txtres"])
  print("- ", end="")
  print(dicres["txtopt"])
