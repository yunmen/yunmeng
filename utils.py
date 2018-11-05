# -*- coding: utf-8 -*-
'''
通用工具函数封装
'''
import os
from datetime import datetime
import uuid
import hashlib


def md5(origin_str):
    '''计算md5'''
    m5 = hashlib.md5()
    try:
        m5.update(origin_str)
    except TypeError:
        m5.update(origin_str.encode('utf-8', 'ignore'))
    except UnicodeEncodeError:
        m5.update(origin_str.encode('utf-8', 'ignore'))
    return m5.hexdigest()

def random_uuid():
    '''获取随机uuid'''
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return uuid.uuid5(uuid.NAMESPACE_DNS, ts).hex

def touch(fname):
    '''创建文件'''
    open(fname, 'a').close()
    os.utime(fname, None)

def datetime_validate(dt_str, dt_fmt):
    '''
    验证时间字符串是否符合指定的格式

    :param dt_str: 时间字符串
    :param dt_fmt: 时间格式
    :type dt_str: str
    :type dt_fmt: str
    :return: 验证是否通过
    :rtype: bool
    '''
    is_ok = False
    try:
        datetime.strptime(dt_str, dt_fmt)
        is_ok = True
    except ValueError:
        pass
    return is_ok

def print_now(prefix='', print_log=None, log_port=None):
    '''
    打印当前时间(%Y-%m-%d %H:%M:%S.%f)
    返回当前时间
    '''
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S.%f')
    msg = '{0}{1}'.format(prefix, now_str)
    if not print_log is None:
        print_log(msg, log_port)
    else:
        print(msg)
    return now

def safe_div(dividend, divisor):
    '''安全除法，防止被0除'''
    return dividend / divisor if divisor != 0 else 0

def sibling_path(reference, file_name, level='.'):
    '''
    根据文件名和参考文件路径，得到与参考文件同级的路径
    '''
    abs_path = os.path.abspath(reference)
    dir_path = os.path.dirname(abs_path)
    for _dot in level[1:]:
        dir_path = os.path.dirname(dir_path)
    return os.path.join(dir_path, file_name)