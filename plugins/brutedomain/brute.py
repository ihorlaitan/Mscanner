#!/usr/bin/python
# -*-coding:utf-8-*-
import os
import time
import dns.resolver

def generate_domain(start_domain = ""):
    '''
    生成待检测的域名列表
    '''
    prefix_list = sorted(list(set([i.replace('\r','').replace('\n','') for i in open("subnames_largest.txt")])))
    next_prefix_list = sorted(list(set([i.replace('\r','').replace('\n','') for i in open("next_sub.txt")])))
    domain_list = []
    for i in prefix_list:
        domain = i + '.' + start_domain
        domain_list.append(domain)

    # for i in prefix_list:
    #     for j in next_prefix_list:
    #         domain = j + '.' + i + '.' + start_domain
    #         domain_list.append(domain)


    domain_list = domain_list[::-1]
    return domain_list



def brute_domain(start_domain = ""):
    urls = generate_domain(start_domain)
    res = dns.resolver.Resolver()           # also tried with configure=False
    # res.nameservers = ['180.76.76.76']
    res.nameservers = ['119.29.29.29','180.76.76.76','182.254.116.116','114.114.114.114','114.114.115.115']

    info_dict = {}
    for url in urls:
        ip_list = []
        try:
            for i in res.query(url).response.answer:
                for item in i.items:
                    item = str(item)
                    if not item.endswith('.'):
                        ip_list.append(item)
                ip_list = sorted(ip_list)
        except Exception as e:
            pass
        if ip_list == []:
            continue
        ip_str = str(ip_list)
        if ip_str in info_dict:
            info_dict[ip_str].add(url)
        else:
            info_dict[ip_str] = set()
            info_dict[ip_str].add(url)
        if len(info_dict[ip_str]) < 2:
            print ip_str,info_dict[ip_str]


def single_test():
    res = dns.resolver.Resolver()           # also tried with configure=False
    url = "1001script.suning.com"
    res.nameservers = ['119.29.29.29','180.76.76.76','182.254.116.116','114.114.114.114','114.114.115.115']
    for i in res.query(url).response.answer:
        ip_list = []
        for item in i.items:
            item = str(item)
            if not item.endswith('.'):
                ip_list.append(item)
        ip_list = sorted(ip_list)


def main():
    url = 'letv.com'
    # url = 'sports.sina.com.cn'
    # print socket.gethostbyname_ex(url)
    # A = dns.resolver.query(url)
    # for i in A.response.answer:
    #     for j in i.items:
    #         print j

    res = dns.resolver.Resolver()           # also tried with configure=False
    # res.nameservers = ['180.76.76.76']
    res.nameservers = ['119.29.29.29','180.76.76.76','182.254.116.116','114.114.114.114','114.114.115.115']

    answer = res.query(url)
    for i in answer.response.answer:
        for j in i.items:
            print j



if __name__ == '__main__':
    brute_domain("suning.com")
    # single_test()
