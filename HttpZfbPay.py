# -*- coding: utf-8 -*-
# @Time    : 2021-01-24 13:35
# @Author  : makun 15902051493
# @FileName: HttpZfbPay.py
# @Describe: 使用http协议直接进行支付宝的支付操作
# https://opendocs.alipay.com/apis/api_28/alipay.fund.trans.uni.transfer

import requests, uuid, hashlib
import json
from datetime import datetime
import GetCertSN, RSAUtil
from urllib.parse import urlencode


# '''md5 hash'''
def md5Hash(tmp):
    try:
        tmp = tmp.encode("utf-8")
        return hashlib.md5(tmp).hexdigest()
    except:
        return hashlib.md5(tmp).hexdigest()


def connectQuerys(querys):
    keyList = []
    for each in querys:
        keyList.append(each)
    keyList = sorted(keyList)
    tmpList = []
    for i in range(0, len(keyList)):
        tmpList.append("{}={}".format(keyList[i], querys.get(keyList[i])))
    result = "&".join(tmpList)
    return result


def getSign(querys):
    tmpStr = connectQuerys(querys)
    # TODO   请补全自己创建应用时创建的私钥
    pri = ''''''
    result = RSAUtil.RSASign(content=tmpStr, private_key=pri, sign_type="RSA2")

    return result


def zfbRequest():
    appId = ""
    url = "https://openapi.alipay.com/gateway.do"

    # TODO 请补全自己的密钥地址
    rootCertSN = GetCertSN.get_root_cn_sn("alipayRootCert.crt")
    appCertSN = GetCertSN.get_app_cert_cn(
        cert_file="appCertPublicKey.crt")

    bizContent = {
        "out_biz_no": md5Hash("{}".format(uuid.uuid4()).encode("UTF-8")),
        "trans_amount": 0.01,  # 这里是金额
        "product_code": "TRANS_ACCOUNT_NO_PWD",
        "biz_scene": "DIRECT_TRANSFER",
        "payee_info": {
            "identity": "13800138000",
            "identity_type": "ALIPAY_LOGON_ID",
            "name": "name"
        }
    }

    querys = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'method': 'alipay.fund.trans.uni.transfer',
        'app_id': appId,
        'sign_type': 'RSA2',
        'version': '1.0',
        'charset': 'utf-8',
        'biz_content': json.dumps(bizContent, separators=(',', ':'), ensure_ascii=False),
        'alipay_root_cert_sn': rootCertSN,
        'app_cert_sn': appCertSN
    }

    sign = getSign(querys)
    querys['sign'] = sign.decode('utf-8')

    url = "{}?{}".format(url, urlencode(querys))

    req = requests.post(url=url)
    content = req.content
    req.close()

    print(content.decode('UTF-8'))


if __name__ == '__main__':
    zfbRequest()
