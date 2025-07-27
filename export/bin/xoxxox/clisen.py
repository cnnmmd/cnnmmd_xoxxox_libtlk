import importlib.util
import argparse
from xoxxox.params import Engine

#---------------------------------------------------------------------------

def getprc(engine):
  s = importlib.util.spec_from_file_location("module", f"{Engine.dirprc}/{engine}.py")
  module = importlib.util.module_from_spec(s)
  s.loader.exec_module(module)
  return module

def infere(txtreq):
  txtres = senprc.infere(txtreq)
  return txtres

#---------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--engine")
parser.add_argument("--config")
objarg = parser.parse_args()
dicprm = {k: v for k, v in vars(objarg).items() if v is not None}

dicprm.pop("engine")
engine = objarg.engine

#---------------------------------------------------------------------------

module = getprc(engine)
senprc = module.SenPrc(**dicprm)
senprc.status(**dicprm)
while True:
  print("> ", end="")
  txtreq = input()
  txtres = infere(txtreq)
  print("< ", end="")
  print(txtres)
