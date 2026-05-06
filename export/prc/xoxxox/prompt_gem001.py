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
    self.frmsys = self.strcon.join([txtsys, "\n\n"])

  @classmethod
  def catreq(self, txtreq):
    frmusr = self.strcon.join(["<start_of_turn>user\n", txtreq, "<end_of_turn>"])
    self.lstlog.append(frmusr)

    tmplog = self.lstlog.copy()
    frmfst = tmplog.pop(0)
    #print("frmfst[" + str(frmfst) + "]", flush=True) # DBG
    lstmch = re.match("^<start_of_turn>user\n(.*)<end_of_turn>$", frmfst)
    txtfst = lstmch.group(1) if lstmch else ""
    frmfst = "".join(["<start_of_turn>user\n", self.frmsys, txtfst, "<end_of_turn>"])
    tmplog.insert(0, frmfst)

    txtprm = self.strlog.join(tmplog) + self.strlog + "<start_of_turn>model"
    return txtprm

  @classmethod
  def catres(self, txtres):
    frmagt = self.strcon.join(["<start_of_turn>model\n", txtres, "<end_of_turn>"])
    self.lstlog.append(frmagt)
    if len(self.lstlog) > self.maxlog:
      self.lstlog.pop(0)
      self.lstlog.pop(0)

  @classmethod
  def arrres(self, txtifr):
    txtres = re.sub("^:", "", txtifr)
    txtres = re.sub("^>", "", txtres)
    return (txtres, "")
