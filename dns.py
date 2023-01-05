# -*- coding: utf-8 -*-

from dnserver import DNSServer, Zone
from tcping_modified import Ping
import os
import zstd
import time
from config import TTL, server, enable_ipv6, domain_list
import sys


class Logger(object):

    def __init__(self, stream=sys.stdout):
        output_dir = "./"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        log_name = 'run_latest.log'
        filename = os.path.join(output_dir, log_name)

        self.terminal = stream
        self.log = open(filename, 'a+',1)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

def set_record(new_ipv4: str, new_ipv6: str = None) -> bool:
    new_dns_list: list[Zone] = []
    for domain in domain_list:
        zone = Zone(host=domain, type='A', answer=new_ipv4)
        zone6 = Zone(host=domain, type='AAAA', answer=new_ipv6)
        new_dns_list.append(zone)
        new_dns_list.append(zone6)
    server.set_records(new_dns_list)


def change_ip() -> str:
    file = open('./file/ip_pool.txt', 'r')
    while True:
        x = file.readline()
        if not x:
            file = open('./file/ip_pool.txt', 'r')
            x = file.readline()
        yield x


def change_ip6() -> str:
    file = open('./file/ip_pool6.txt', 'r')
    while True:
        x = file.readline()
        if not x:
            file = open('./file/ip_pool.txt', 'r')
            x = file.readline()
        yield x


def tcping(ip: str, ipv6: bool = False) -> bool:
    p = Ping(ip, port=443, timeout=2)
    p.ping(count=1, ipv6=ipv6)
    return True if p._successed == 1 else False


def choose_v4(ipv4, gen_ip, ipv6) -> bool:
    ping_n = tcping(ipv4)
    if not ping_n:
        ipv4 = next(gen_ip)
        ipv4 = ipv4.rstrip('\n')
        print(f'Warn: Current ip is down. Choosing "{ipv4}".')
        set_record(ipv4, ipv6)
        return False, ipv4
    else:
        return True, ipv4


def choose_v6(ipv6, gen_ipv6, ipv4) -> bool:
    ping_6 = tcping(ipv6, ipv6=True)
    if not ping_6:
        ipv6: str = next(gen_ipv6)
        ipv6 = ipv6.rstrip('\n')
        print(f'Warn: Current ipv6 is down. Choosing "{ipv6}".')
        set_record(ipv4, ipv6)
        return False, ipv6
    else:
        return True, ipv6


if __name__ == '__main__':
    if os.path.exists('./run_latest.log'):
        with open(f'./run{time.time()}.log.zst', 'wb') as zst:
            zst.write(zstd.compress(open('./run_latest.log', 'rb').read()))
        os.remove('./run_latest.log')
    sys.stdout = Logger(sys.stdout)
    sys.stderr = Logger(sys.stderr)
    n = m = False
    gen_ip = change_ip()
    gen_ipv6 = change_ip6()
    ipv4: str = next(gen_ip)
    ipv4 = ipv4.rstrip('\n')
    print(f'Choosing "{ipv4}".')
    if enable_ipv6:
        ipv6: str = next(gen_ipv6)
        ipv6 = ipv6.rstrip('\n')
        print(f'Choosing "{ipv6}".')
    else:
        ipv6 = None
    set_record(ipv4, ipv6)
    server.start()
    while server.is_running:
        counter = 0
        n, ipv4 = choose_v4(ipv4, gen_ip, ipv6)
        while not n:
            n, ipv4 = choose_v4(ipv4, gen_ip, ipv6)
            counter += 1
            if counter > 10:
                break

        if enable_ipv6:
            counter = 0
            m, ipv6 = choose_v6(ipv6, gen_ipv6, ipv4)
            while not m:
                m, ipv6 = choose_v6(ipv6, gen_ipv6, ipv4)
                counter += 1
                if counter > 10:
                    break

        print(f'Ip is good now.')
        time.sleep(TTL)
