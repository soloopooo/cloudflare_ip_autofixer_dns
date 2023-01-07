# -*- coding: utf-8 -*-

from typing import Any, Callable, Iterable, Mapping
from dnserver import DNSServer, Zone
from tcping_modified import Ping
import os
import zstd
import time
from config import TTL, server, enable_ipv6, domain_list, tcping_times, tcping_success_times, pause_times_no_ip, ttl_interval_add, check_thread
import sys
import logging
from threading import Thread
import random


class Logger(object):

    def __init__(self, stream=sys.stdout):
        output_dir = "./logs/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        log_name = 'run_latest.log'
        filename = os.path.join(output_dir, log_name)

        self.terminal = stream
        self.log = open(filename, 'a+', 1)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(
    '%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

logger_in = logging.getLogger(__name__)
logger_in.addHandler(handler)
logger_in.setLevel(logging.INFO)


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
    p.ping(count=tcping_times, ipv6=ipv6)
    return True if p._successed >= tcping_success_times else False


class TcpingThreading(Thread):
    def __init__(self, func, args=(), kwargs={}):
        super(TcpingThreading, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.result = self.func(*self.args, **self.kwargs)

    def get_result(self):
        Thread.join(self)
        try:
            return self.result
        except Exception:
            return None


def choose_v4(ipv4, gen_ip, ipv6) -> bool:
    ping_n = tcping(ipv4)
    ip_list = []
    ip_checking_dict = {}
    result_dict = {}
    passed_ip = []
    if not ping_n:
        logger_in.warning(
            f'Warn: Current ip is down. Open {check_thread} threads to test...')
        for i in range(check_thread):
            next_ip = next(gen_ip).rstrip('\n')
            logger_in.info(f'Will test "{next_ip}".')
            ip_list.append(next_ip)
            for ip in ip_list:
                m = TcpingThreading(func=tcping, args=(ip, False))
                ip_checking_dict.update({ip: m})
        for ip, check in ip_checking_dict.items():
            check.start()
        for ip, check in ip_checking_dict.items():
            result_dict.update({ip: check.get_result()})
        for ip, check_result in result_dict.items():
            if check_result:
                logger_in.info(f'{ip} Passed.')
                passed_ip.append(ip)
            else:
                logger_in.info(f'{ip} Failed.')
        try:
            ipv4_prev = ipv4
            ipv4 = random.choice(passed_ip)
            if ipv4:
                logger_in.info(f'Use {ipv4}.')
                return True, ipv4
        except:
            ipv4 = ipv4_prev
            logger_in.warning(f'No ip is suitable. Keeping {ipv4}.')
            return False, ipv4_prev
    else:
        return True, ipv4


def choose_v6(ipv6, gen_ipv6, ipv4) -> bool:
    ping_6 = tcping(ipv6, ipv6=True)
    ip_list = []
    ip_checking_dict = {}
    result_dict = {}
    passed_ip = []
    if not ping_6:
        logger_in.warning(
            f'Warn: Current ipv6 is down. Open {check_thread} threads to test...')
        for i in range(check_thread):
            next_ip = next(gen_ipv6).rstrip('\n')
            logger_in.info(f'Will test "{next_ip}".')
            ip_list.append(next_ip)
            for ip in ip_list:
                m = TcpingThreading(func=tcping, args=(ip, True))
                ip_checking_dict.update({ip: m})
        for ip, check in ip_checking_dict.items():
            check.start()
        for ip, check in ip_checking_dict.items():
            result_dict.update({ip: check.get_result()})
        for ip, check_result in result_dict.items():
            if check_result:
                logger_in.info(f'{ip} Passed.')
                passed_ip.append(ip)
            else:
                logger_in.info(f'{ip} Failed.')
        try:
            ipv6_prev = ipv6
            ipv6 = random.choice(passed_ip)
            if ipv6:
                logger_in.info(f'Use {ipv6}.')
                return True, ipv4
        except:
            ipv6 = ipv6_prev
            logger_in.warning(f'No ip is suitable. Keeping {ipv6}.')
            return False, ipv6_prev
    else:
        return True, ipv6


if __name__ == '__main__':

    if os.path.exists('./logs/run_latest.log'):
        with open(f'./logs/run{time.time()}.log.zst', 'wb') as zst:
            zst.write(zstd.compress(open('./logs/run_latest.log', 'rb').read()))
        os.remove('./logs/run_latest.log')
    sys.stdout = Logger(sys.stdout)
    sys.stderr = Logger(sys.stderr)
    ttl_now = TTL
    n = m = False
    gen_ip = change_ip()
    gen_ipv6 = change_ip6()
    ipv4: str = next(gen_ip)
    ipv4 = ipv4.rstrip('\n')
    logger_in.info(f'Choosing "{ipv4}".')
    if enable_ipv6:
        ipv6: str = next(gen_ipv6)
        ipv6 = ipv6.rstrip('\n')
        logger_in.info(f'Choosing "{ipv6}".')
    else:
        ipv6 = None
    set_record(ipv4, ipv6)
    os.system('ipconfig /flushdns')
    server.start()

    while server.is_running:
        try:
            counter = 0
            n, ipv4 = choose_v4(ipv4, gen_ip, ipv6)
            while not n:
                n, ipv4 = choose_v4(ipv4, gen_ip, ipv6)
                os.system('ipconfig /flushdns')
                counter += 1
                ttl_now = TTL
                if counter > pause_times_no_ip:
                    logger_in.warning(f'Can\'t find ipv4, exiting.')
                    break
            if enable_ipv6:
                counter = 0
                m, ipv6 = choose_v6(ipv6, gen_ipv6, ipv4)
                while not m:
                    m, ipv6 = choose_v6(ipv6, gen_ipv6, ipv4)
                    os.system('ipconfig /flushdns')
                    counter += 1
                    ttl_now = TTL
                    if counter > pause_times_no_ip:
                        logger_in.warning(f'Can\'t find ipv6, exiting.')
                        break
            logger_in.info(f'Ip checking is ok now.')
            logger_in.info(f'Current check interval: {ttl_now}s.')
            time.sleep(ttl_now)
            ttl_now += ttl_interval_add
        except Exception as e:
            logger_in.error(f"Please Check your network.\n{e}")
            logger_in.info("Retrying to connect...")
        except KeyboardInterrupt:
            logger_in.info("Stopping! ...")
            server.stop()
            break
