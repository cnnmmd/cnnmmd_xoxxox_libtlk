#---------------------------------------------------------------------------
# 参照

import re

#---------------------------------------------------------------------------
# 構築：プロンプト：シナリオ形式

class ConLog:

  @classmethod
  def catsys(self, diccnf):
    self.lsthed = []
    self.lstbdy = []
    self.frmsys = "{elmsys}\n"
    self.frmusr = "{txtsrc}{txtdef}{elmusr}\n"
    self.frmagt = "{txtdst}{txtdef}{elmagt}\n"
    # 設定：個別
    self.maxbdy = diccnf["maxlog"]
    self.nulagt = diccnf["nuloth"]
    self.dictlk = {
      "elmsys": diccnf["status"],
      "txtsrc": diccnf["rolslf"],
      "txtdst": diccnf["roloth"],
      "elmusr": diccnf["inislf"],
      "elmagt": diccnf["inioth"],
      "txtdef": "＞",
    }
    self.lsthed.append(self.frmsys.format_map(self.dictlk))
    self.lstbdy.append(self.frmusr.format_map(self.dictlk))
    self.lstbdy.append(self.frmagt.format_map(self.dictlk))

  @classmethod
  def catreq(self, txtreq):
    self.dictlk["elmusr"] = txtreq
    self.lstbdy.append(self.frmusr.format_map(self.dictlk))
    txtprm = "".join(self.lsthed + self.lstbdy)
    return txtprm

  @classmethod
  def catres(self, txtres):
    self.dictlk["elmagt"] = txtres
    self.lstbdy.append(self.frmagt.format_map(self.dictlk))
    if len(self.lstbdy) > self.maxbdy * 2:
      self.lstbdy.pop(0)
      self.lstbdy.pop(0)

  @classmethod
  def arrres(self, txtifr):
    try:
      txtres = re.findall(self.dictlk["txtdst"] + self.dictlk["txtdef"] + "(.*)", txtifr)[0]
    except Exception as e:
      txtres = ""
    if txtres == "":
      txtres = self.nulagt
    return (txtres, "")
