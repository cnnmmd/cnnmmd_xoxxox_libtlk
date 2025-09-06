#---------------------------------------------------------------------------
# 参照

import re

#---------------------------------------------------------------------------
# 構築：プロンプト：試験：sys / usr / agt

class ConLog:
  strcon = ""
  strlog = "\n"

  @classmethod
  def catsys(self, diccnf):
    txtsys = diccnf["status"]
    self.maxlog = diccnf["maxlog"] + 2
    self.lstsys = []
    self.lstlog = []
    frmsys = self.strcon.join(["<|sys|>", txtsys, "<|end|>"])
    self.lstsys.append(frmsys)

  @classmethod
  def catreq(self, txtreq):
    frmusr = self.strcon.join(["<|usr|>", txtreq, "<|end|>"])
    self.lstlog.append(frmusr)
    txtlog = self.strlog.join(["".join(self.lstsys), self.strlog.join(self.lstlog), "<|agt|>"]) + self.strcon
    return txtlog

  @classmethod
  def catres(self, txtres):
    frmagt = self.strcon.join(["<|agt|>", txtres, "<|end|>"])
    self.lstlog.append(frmagt)
    if len(self.lstlog) > self.maxlog:
      self.lstlog.pop(0)
      self.lstlog.pop(0)

  @classmethod
  def arrres(self, txtifr):
    txtres = re.sub(r"\s*<\|end\|>.*", "", txtifr, flags=re.DOTALL).strip()
    return (txtres, "")
