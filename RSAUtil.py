# -*- coding: utf-8 -*-
# @Time    : 2021-01-24 14:08
# @Author  : makun 15902051493
# @FileName: RSAUtil.py
# @Describe: 创建RSA签名
# pip install rsa -i https://pypi.douban.com/simple

import rsa
import base64

__pem_begin = '-----BEGIN RSA PRIVATE KEY-----\n'
__pem_end = '\n-----END RSA PRIVATE KEY-----'


def RSASign(content, private_key, sign_type):
    if sign_type.upper() == 'RSA':
        return rsa_sign(content, private_key, 'SHA-1')
    elif sign_type.upper() == 'RSA2':
        return rsa_sign(content, private_key, 'SHA-256')
    else:
        raise Exception('sign_type错误')


def rsa_sign(content, private_key, _hash):
    private_key = _format_private_key(private_key)
    pri_key = rsa.PrivateKey.load_pkcs1(private_key.encode('utf-8'))
    try:
        sign_result = rsa.sign(content, pri_key, _hash)
    except:
        sign_result = rsa.sign(content.encode("UTF-8"), pri_key, _hash)
    return base64.b64encode(sign_result)


def _format_private_key(private_key):
    if not private_key.startswith(__pem_begin):
        private_key = __pem_begin + private_key
    if not private_key.endswith(__pem_end):
        private_key = private_key + __pem_end
    return private_key
