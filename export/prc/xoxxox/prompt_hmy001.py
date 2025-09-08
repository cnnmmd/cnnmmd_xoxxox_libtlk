#---------------------------------------------------------------------------
# 参照

import re

#---------------------------------------------------------------------------
# 構築：プロンプト：推論取得：gpt-oss (harmony)

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
      "# Valid channels: analysis, commentary, final. Channel must be included for every message."
    frmhed = self.strlog.join(["<|start|>system<|message|>", txthed, "<|end|>"])
    frmdev = self.strcon.join(["<|start|>developer<|message|>", txtsys, "<|end|>"])
    frmsys = self.strlog.join([frmhed, frmdev])
    self.lstsys.append(frmsys)

  @classmethod
  def catreq(self, txtreq):
    frmusr = self.strcon.join(["<|start|>user<|message|>", txtreq, "<|end|>"])
    self.lstlog.append(frmusr)
    txtprm = self.strlog.join(["".join(self.lstsys), self.strlog.join(self.lstlog), "<|start|>assistant"]) + self.strcon
    return txtprm

  @classmethod
  def catres(self, txtres):
    frmagt = self.strcon.join(["<|start|>assistant<|channel|>final<|message|>", txtres, "<|end|>"])
    self.lstlog.append(frmagt)
    if len(self.lstlog) > self.maxlog:
      self.lstlog.pop(0)
      self.lstlog.pop(0)

  @classmethod
  def arrres(self, txtifr):
    l = re.findall(
      r"<\|channel\|>analysis<\|message\|>(.*?)<\|end\|>",
      txtifr,
      flags=re.DOTALL
    )
    txtana = "\n".join([a.strip() for a in l])
    m = re.search(
      r"<\|channel\|>final<\|message\|>(.*?)(?:<\|return\|>|<\|end\|>|$)",
      txtifr,
      flags=re.DOTALL
    )
    txtres = m.group(1).strip() if m else ""
    return (txtres, txtana)
