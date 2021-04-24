# 用于向指定支付宝账户转账
这是一份python原生实现的支付宝“用于向指定支付宝账户转账”功能的代码，您只需要做以下事情：

打开HttpZfbPay.py文件
1. 第37行，将您创建应用时的私钥补充进来；
2. 第48-51行，将创建应用时的根证书和应用公钥补充路径；
3. 第53-74行，每一个参数请根据实际情况填充，具体参数说明看文档：https://opendocs.alipay.com/apis/api_28/alipay.fund.trans.uni.transfer
4. HttpZfbPay.py文件的zfbRequest() 函数是具体调用函数，触发转账通过该函数即可触发