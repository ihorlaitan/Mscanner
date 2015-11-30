#!/usr/bin/python
# -*-coding:utf-8-*-
import os
import time
import dns.resolver
import Queue
import threading

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


domains_queue = Queue.Queue()
info_queue = Queue.Queue()

def server(start_domain):
    global domains_queue
    for i in generate_domain(start_domain):
        domains_queue.put(i)
    print 'start!!'

    threads = []

    for i in xrange(10):
        thread = threading.Thread(target = brute_work)
        threads.append(thread)

    thread = threading.Thread(target = print_work)
    threads.append(thread)

    for i in threads:
        i.setDaemon(True)
        i.start()

    while True:
        pass


def brute_work():
    global domains_queue
    global info_queue

    res = dns.resolver.Resolver()
    res.nameservers = ['119.29.29.29','180.76.76.76','182.254.116.116','114.114.114.114','114.114.115.115']

    while True:
        if domains_queue.qsize() > 0:
            domain = domains_queue.get()
            ip_list = []
            try:
                for i in res.query(domain).response.answer:
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
            info = (domain,ip_str)
            info_queue.put(info)
        else:
            time.sleep(1)




def print_work():
    global info_queue
    info_dict = {}
    while True:
        if info_queue.qsize() > 0:
            info = info_queue.get()
            domain,ip_str = info

            if ip_str in info_dict:
                info_dict[ip_str].add(domain)
            else:
                info_dict[ip_str] = set()
                info_dict[ip_str].add(domain)

            if len(info_dict[ip_str]) < 2:
                print ip_str,info_dict[ip_str]

        else:
            time.sleep(1)


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
    try:
        server("suning.com")
    except KeyboardInterrupt:
        print "User Press Ctrl+C,Exit"
    except EOFError:
        print "User Press Ctrl+D,Exit"

    # single_test()
