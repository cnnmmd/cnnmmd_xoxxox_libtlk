import importlib.util
import argparse
import asyncio
from xoxxox.params import Engine

#---------------------------------------------------------------------------

def getprc(engine):
  s = importlib.util.spec_from_file_location("module", f"{Engine.dirprc}/{engine}.py")
  module = importlib.util.module_from_spec(s)
  s.loader.exec_module(module)
  return module

def infere(txtreq):
  if gensyn == "1":
    txtres = tttprc.infere(txtreq)
  else:
    txtres = asyncio.run(tttprc.infere(txtreq))
  return txtres

#---------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--engine", default="gpt")
parser.add_argument("--gensyn", default="1")
parser.add_argument("--config")
parser.add_argument("--prmmax", type=int)
parser.add_argument("--status")
parser.add_argument("--rolslf")
parser.add_argument("--roloth")
parser.add_argument("--inislf")
parser.add_argument("--inioth")
objarg = parser.parse_args()
dicprm = {k: v for k, v in vars(objarg).items() if v is not None}

dicprm.pop("engine")
dicprm.pop("gensyn")
engine = objarg.engine
gensyn = objarg.gensyn

#---------------------------------------------------------------------------

module = getprc(engine)
tttprc = module.TttPrc(**dicprm)
tttprc.status(**dicprm)
while True:
  print("> ", end="")
  txtreq = input()
  txtres = infere(txtreq)
  print("< ", end="")
  print(txtres)
