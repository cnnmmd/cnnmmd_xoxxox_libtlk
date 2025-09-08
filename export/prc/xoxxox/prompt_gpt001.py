#---------------------------------------------------------------------------
# 構築：プロンプト：試験：gpt

class ConLog:

  @classmethod
  def catsys(self, diccnf):
    txtsys = diccnf["status"]
    self.maxlog = diccnf["maxlog"] + 2
    self.lstsys = []
    self.lstlog = []
    dicsys = {"role": "system", "content": txtsys}
    self.lstsys.append(dicsys)

  @classmethod
  def catreq(self, txtreq):
    dicusr = {"role": "user", "content": txtreq}
    self.lstlog.append(dicusr)
    lstprm = []
    lstprm.extend(self.lstsys)
    lstprm.extend(self.lstlog)
    return lstprm

  @classmethod
  def catres(self, txtres):
    dicagt = {"role": "assistant", "content": txtres}
    self.lstlog.append(dicagt)
    if len(self.lstlog) > self.maxlog:
      self.lstlog.pop(0)
      self.lstlog.pop(0)

  @classmethod
  def arrres(self, txtifr):
    txtres = txtifr
    return (txtres, "")
