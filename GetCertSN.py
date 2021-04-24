# -*- coding: utf-8 -*-
# @Time    : 2021-01-24 13:58
# @Author  : makun 15902051493
# @FileName: GetCertSN.py
# @Describe: 获取证书序列号
import OpenSSL
import hashlib
import re


def md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


# 应用公钥证书序列号
def get_app_cert_cn(cert_str=None, cert_file=None):
    cert_str = cert_str or open(cert_file).read()
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_str)
    try:
        res = cert.get_signature_algorithm()
        if not re.match(b'sha.+WithRSAEncryption', res):
            return None
    except:
        return None
    cert_issue = cert.get_issuer()
    op = ''
    b = list(cert_issue.get_components())
    for i in range(len(b)):
        a = list(b[len(b) - 1 - i])
        opp = "{}={}".format(a[0].decode(), a[1].decode())
        op = op + opp + ','
    return md5(op[:-1] + str(cert.get_serial_number()))


# 根证书序列号
def get_root_cn_sn(cert_file):
    root_cert = open(cert_file).read()
    cert_list = root_cert.split('-----BEGIN CERTIFICATE-----')
    root_cert_sn = ''
    for i in cert_list:
        if not len(i):
            continue
        cert_sn = get_app_cert_cn('-----BEGIN CERTIFICATE-----' + i)
        if cert_sn is not None:
            root_cert_sn = root_cert_sn + cert_sn + '_'
    return root_cert_sn[:-1]
