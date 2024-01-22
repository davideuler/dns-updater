#coding=utf-8
import json,re,os
import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from datetime import datetime



from config import *
from myip import config_ip

from aliyunsdkcore.client import AcsClient

previous_ip = config_ip
my_ip_file = 'myip.py'

#通过ip.cn网站获取外网ip地址
def get_now_ip():
    url="http://cip.cc"
    url="https://ifconfig.me"
    headers = { 'User-Agent': "curl/10.0","Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    response = requests.get(url,headers=headers)
    now_ip = response.content.decode("utf-8")
    #print("current ip address:%s" % (now_ip))
    return (now_ip)

now_ip = get_now_ip()

if not now_ip == previous_ip:
    print("Gonna to update ip:" + get_now_ip())
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H%M%S")
    content = "config_ip='%s'; update_date='%s'" % (now_ip,formatted_datetime)
    with open(my_ip_file, 'a') as file:
        # Write the text content to the file
        file.write(content)
