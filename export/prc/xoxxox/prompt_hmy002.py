#---------------------------------------------------------------------------
# 参照

import re

#---------------------------------------------------------------------------
# 構築：プロンプト：応答のみ：gpt-oss (harmony)

class ConLog:
  strcon = ""
  strlog = "\n"

  @classmethod
  def catsys(self, diccnf):
    txtsys = diccnf["status"]
    self.maxlog = diccnf["maxlog"] + 2
    self.lstsys = []
    self.lstlog = []
    txthed = \
      "You are ChatGPT, a large language model trained by OpenAI.\n\n"\
      "Reasoning: low\n\n"\
      "# Valid channels: final. Channel must be included for every message."
    frmhed = self.strlog.join(["<|start|>system<|message|>", txthed, "<|end|>"])
    frmdev = self.strcon.join(["<|start|>developer<|message|>", txtsys, "<|end|>"])
    frmsys = self.strlog.join([frmhed, frmdev])
    self.lstsys.append(frmsys)

  @classmethod
  def catreq(self, txtreq):
    frmusr = self.strcon.join(["<|start|>user<|message|>", txtreq, "<|end|>"])
    self.lstlog.append(frmusr)
    txtlog = self.strlog.join(["".join(self.lstsys), self.strlog.join(self.lstlog), "<|start|>assistant<|channel|>final<|message|>"]) + self.strcon
    return txtlog

  @classmethod
  def catres(self, txtres):
    frmagt = self.strcon.join(["<|start|>assistant<|channel|>final<|message|>", txtres, "<|end|>"])
    self.lstlog.append(frmagt)
    if len(self.lstlog) > self.maxlog:
      self.lstlog.pop(0)
      self.lstlog.pop(0)

  @classmethod
  def arrres(self, txtifr):
    txtres = re.sub(r"\s*<\|return\|>.*", "", txtifr, flags=re.DOTALL).strip()
    return (txtres, "")
