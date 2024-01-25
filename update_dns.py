#coding=utf-8
import json,re,os
import requests
from datetime import datetime

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest

from config import *
from myip import config_ip

from aliyunsdkcore.client import AcsClient

previous_ip = config_ip
my_ip_file = 'myip.py'
ipv4_flag = True

# Initialize the AcsClient
client = AcsClient(aliyun_ak, aliyun_sk, 'cn-hangzhou')

#通过ip.cn网站获取外网ip地址
def get_now_ip():
    url="http://cip.cc"
    url="https://ifconfig.me"
    headers = { 'User-Agent': "curl/10.0","Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    response = requests.get(url,headers=headers)
    now_ip = response.content.decode("utf-8")
    #print("current ip address:%s" % (now_ip))
    return (now_ip)


def update(RecordId, RR, Type, Value):  # 修改域名解析记录
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_RecordId(RecordId)
    request.set_RR(RR)
    request.set_Type(Type)
    request.set_Value(Value)
    response = client.do_action_with_exception(request)


def add(DomainName, RR, Type, Value):  # 添加新的域名解析记录
    request = AddDomainRecordRequest()
    request.set_accept_format('json')
    request.set_DomainName(DomainName)
    request.set_RR(RR)  
    request.set_Type(Type)
    request.set_Value(Value)    
    response = client.do_action_with_exception(request)


def update_domain_to_ip(ip):
  if ipv4_flag == 1:
    request = DescribeSubDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain)
    request.set_SubDomain(name_ipv4 + '.' + domain)
    request.set_Type("A")
    response = client.do_action_with_exception(request)  
    domain_list = json.loads(response)  

    ipv4 = ip

    if domain_list['TotalCount'] == 0:
        add(domain, name_ipv4, "A", ipv4)
        print("dns created successfully")
    elif domain_list['TotalCount'] == 1:
        if domain_list['DomainRecords']['Record'][0]['Value'].strip() != ipv4.strip():
            update(domain_list['DomainRecords']['Record'][0]['RecordId'], name_ipv4, "A", ipv4)
            print("dns updated successfully")
        else: 
            print("IPv4 addr not changed")
    elif domain_list['TotalCount'] > 1:
        from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest
        request = DeleteSubDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(domain) 
        request.set_RR(name_ipv4)
        request.set_Type("A") 
        response = client.do_action_with_exception(request)
        add(domain, name_ipv4, "A", ipv4)
        print("dns updated successfully")


  else: #if ipv6_flag == 1:
    request = DescribeSubDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain)
    request.set_SubDomain(name_ipv6 + '.' + domain)
    request.set_Type("AAAA")
    response = client.do_action_with_exception(request) 
    domain_list = json.loads(response) 

    ipv6 = ip

    if domain_list['TotalCount'] == 0:
        add(domain, name_ipv6, "AAAA", ipv6)
        print("dns created successfully")
    elif domain_list['TotalCount'] == 1:
        if domain_list['DomainRecords']['Record'][0]['Value'].strip() != ipv6.strip():
            update(domain_list['DomainRecords']['Record'][0]['RecordId'], name_ipv6, "AAAA", ipv6)
            print("dns updated successfully")
        else:  
            print("IPv6 addr not changed")
    elif domain_list['TotalCount'] > 1:
        from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest
        request = DeleteSubDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(domain)
        request.set_RR(name_ipv6)  
        request.set_Type("AAAA") 
        response = client.do_action_with_exception(request)
        add(domain, name_ipv6, "AAAA", ipv6)
        print("dns updated successfully")

now_ip = get_now_ip()

if not now_ip == previous_ip:
    print("Gonna to update ip:" + get_now_ip())
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H%M%S")
    content = "config_ip='%s'; update_date='%s';\n" % (now_ip,formatted_datetime)
    with open(my_ip_file, 'a') as file:
        # Write the text content to the file
        file.write(content)
    update_domain_to_ip(now_ip)
