#---------------------------------------------------------------------------
# 参照

import aiohttp
from xoxxox.libmid import LibMid

#---------------------------------------------------------------------------
# 処理：ＳＴＴ

class PrcStt:

  # 変換：サウンド → テキスト
  @staticmethod
  async def cnnstt(datorg, server, config):
    async with aiohttp.ClientSession() as sssweb:
      async with sssweb.post(server + "/gen", data=datorg) as datres:
        dicres = await datres.json()
    txtres = dicres["txtres"]
    datnew = txtres.encode("utf-8")
    return datnew

LibMid.dicprc.append({"key": "xoxxox.PrcStt.cnnstt", "frm": "LibMid.plugin['xoxxox_libtlk'].PrcStt.cnnstt(values[dicreq['keydat']], dicreq['server'], dicreq['config'])", "syn": False})

#---------------------------------------------------------------------------
# 処理：ＴＴＳ

class PrcTts:

  # 変数
  oldcfg = ""

  # 変換：テキスト → サウンド
  @staticmethod
  async def cnntts(datorg, server, config):

    if config != PrcTts.oldcfg:
      async with aiohttp.ClientSession() as sssweb:
        async with sssweb.post(server + "/sys", json={"config": config}) as datres:
          dicres = await datres.json()
      PrcTts.oldcfg = config
    
    async with aiohttp.ClientSession() as sssweb:
      async with sssweb.post(server + "/gen", json={"txtreq": datorg.decode("utf-8")}) as datres:
        rawres = await datres.read()
    return rawres

LibMid.dicprc.append({"key": "xoxxox.PrcTts.cnntts", "frm": "LibMid.plugin['xoxxox_libtlk'].PrcTts.cnntts(values[dicreq['keydat']], dicreq['server'], dicreq['config'])", "syn": False})

#---------------------------------------------------------------------------
# 処理：ＴＴＴ

class PrcTtt:

  # 変数
  oldcfg = ""

  # 生成：テキスト → テキスト
  @staticmethod
  async def cnnttt(datorg, server, config):

    if config != PrcTtt.oldcfg:
      async with aiohttp.ClientSession() as sssweb:
        async with sssweb.post(server + "/sys", json={"config": config}) as datres:
          dicres = await datres.json()
      PrcTtt.oldcfg = config

    async with aiohttp.ClientSession() as sssweb:
      async with sssweb.post(server + "/gen", json={"txtreq": datorg.decode("utf-8")}) as datres:
        dicres = await datres.json()
    txtres = dicres["txtres"]
    datnew = txtres.encode("utf-8")
    return datnew

LibMid.dicprc.append({"key": "xoxxox.PrcTtt.cnnttt", "frm": "LibMid.plugin['xoxxox_libtlk'].PrcTtt.cnnttt(values[dicreq['keydat']], dicreq['server'], dicreq['config'])", "syn": False})

#---------------------------------------------------------------------------
# 処理：感情分析

class PrcSen:

  # 変数
  oldcfg = ""

  # 変換：テキスト → テキスト
  @staticmethod
  async def cnnsen(datorg, server, config):

    if config != PrcSen.oldcfg:
      async with aiohttp.ClientSession() as sssweb:
        async with sssweb.post(server + "/sys", json={"config": config}) as datres:
          dicres = await datres.json()
      PrcSen.oldcfg = config

    async with aiohttp.ClientSession() as sssweb:
      async with sssweb.post(server + "/gen", json={"txtreq": datorg.decode("utf-8")}) as datres:
        dicres = await datres.json()
        txtres = dicres["txtres"]
        datnew = txtres.encode("utf-8")
        return datnew

LibMid.dicprc.append({"key": "xoxxox.PrcSen.cnnsen", "frm": "LibMid.plugin['xoxxox_libtlk'].PrcSen.cnnsen(values[dicreq['keydat']], dicreq['server'], dicreq['config'])", "syn": False})
