# -*- coding: utf-8 -*-
# @Time    : 2021/11/9 5:01 下午
# @Author  : tingbai
# @Email   : 490336534@qq.com
# @File    : tools.py
# @Desc    : 零散方法
import base64
import os
import random
import string
import urllib.parse
from faker import Faker

fk = Faker(locale='zh_CN')


def random_mobile():
    """随机生成手机号"""
    return fk.phone_number()


def random_msisdn():
    return fk.msisdn()


def random_name():
    """随机生成中文名字"""
    return fk.name()


def random_ssn():
    """随机生成一个身份证号"""
    return fk.ssn()


def random_addr():
    """随机生成一个地址"""
    return fk.address()


def random_city():
    """随机生成一个城市名"""
    return fk.city()


def random_company():
    """随机生成一个公司名"""
    return fk.company()


def random_postcode():
    """随机生成一个邮编"""
    return fk.postcode()


def random_email():
    """随机生成一个邮箱号"""
    return fk.email()


def random_date():
    """随机生成一个日期"""
    return fk.date()


def radom_date_time():
    """随机生成一个时间"""
    return fk.date_time()


def random_ipv4():
    """随机生成一个ipv4的地址"""
    return fk.ipv4()


def random_job():
    """随机生成一个职业"""
    return fk.job()


def base64_encode(data: str):
    """base64编码"""
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def md5_encrypt(data: str):
    """md5加密"""
    from hashlib import md5
    new_md5 = md5()
    new_md5.update(data.encode('utf-8'))
    return new_md5.hexdigest()


def rsa_encrypt(msg, server_pub):
    """
    rsa加密
    :param msg: 待加密文本
    :param server_pub: 密钥
    :return:
    """
    import rsa

    msg = msg.encode('utf-8')
    pub_key = server_pub.encode("utf-8")
    public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
    cryto_msg = rsa.encrypt(msg, public_key_obj)  # 生成加密文本
    cipher_base64 = base64.b64encode(cryto_msg)  # 将加密文本转化为 base64 编码
    return cipher_base64.decode()


def get_url(url, type=True):
    """
    url转码
    type=True: %E6%88%91%E8%A6%81%E5%8F%8D%E9%A6%88 =》我要反馈
    type=False: 我要反馈 =》%E6%88%91%E8%A6%81%E5%8F%8D%E9%A6%88
    """
    if type:
        return urllib.parse.unquote(url)
    else:
        return urllib.parse.quote(url)


def random_letters_digits(num):
    """
    获取指定个数的随机字符串和数字
    :param num:
    :return:
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, num))


def set_apk_version(apk_version):
    print(f"apk_version:{apk_version}")
    os.environ['apk_version'] = apk_version


def name_mosaic(name):
    """
    姓名脱敏
    @param name:
    @return:
    """
    if len(name) == 2:
        name_mosaic = name[0] + '*'
    elif len(name) == 3:
        name_mosaic = name[0] + '*' + name[-1]
    elif len(name) > 3:
        name_mosaic = name[:2] + '*' * (len(name) - 2)
    else:
        name_mosaic = name
    return name_mosaic


def ms2s(value):
    return round(value / 1000.0, 2)


def transfer_temp(temp):
    return round(temp / 10.0, 1)


def mV2V(v):
    return round(v / 1000.0, 2)


def uA2mA(c):
    return round(c / 1000.0, 2)
