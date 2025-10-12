#---------------------------------------------------------------------------
# 参照

#---------------------------------------------------------------------------
# 構築：プロンプト：[INST] - [/INST]

class ConLog:

  @classmethod
  def genprm(self, lstsys, lstusr, lstagt):
    prompt = ""
    i = 0
    while i < len(lstusr):
      if i == 0:
        strfst = "<s>" + "[INST]" + "<<SYS>>" + "".join(self.lstsys) + "<</SYS>>" + lstusr[i] + "[/INST]"
        if i == len(lstusr) - 1:
          prompt = strfst
        else:
          prompt = strfst + lstagt[i]
      else:
        stroth = "</s>" + "\n" + "<s>" + "[INST]" + lstusr[i] + "[/INST]"
        if i == len(lstusr) - 1:
          prompt = prompt + stroth
        else:
          prompt = prompt + stroth +  lstagt[i]
      i = i + 1
    return prompt

  @classmethod
  def catsys(self, diccnf):
    txtsys = diccnf["status"]
    self.maxlog = diccnf["maxlog"] - 1
    self.lstsys = []
    self.lstusr = []
    self.lstagt = []
    self.lstsys.append(txtsys)

  @classmethod
  def catreq(self, txtreq):
    self.lstusr.append(txtreq)
    txtprm = self.genprm(self.lstsys, self.lstusr, self.lstagt)
    return txtprm

  @classmethod
  def catres(self, txtres):
    self.lstagt.append(txtres)
    if len(self.lstusr) > self.maxlog:
      self.lstusr.pop(0)
      self.lstagt.pop(0)

  @classmethod
  def arrres(self, txtifr):
    txtres = txtifr
    e = min(
      txtres.find("<") if "<" in txtres else len(txtres),
      txtres.find("[") if "[" in txtres else len(txtres)
    )
    txtres = txtres[:e]
    txtres = txtres.replace(" ", "")
    txtres = txtres.replace("\n", "")
    return (txtres, "")
