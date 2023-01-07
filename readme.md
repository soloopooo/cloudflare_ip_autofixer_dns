## Cloudflare ip autofixer -- dns

A local DNS server with IP changing and balancing, and unblocking.

[简体中文](readme_zhcn.md)

It CAN be worked on other cdns. try your own!

## What do you need?

You need python 3.11.0.

run `pip install -r requirements.txt`.

Open `config.py`. You can config your dns list, upstream DNS server(8.8.8.8 or 223.5.5.5).

Make sure you have input some ip addresses in `./file/ip_pool.txt`.

IP pool can be changed in directories `./file/`.

Then run `python3 dns.py`.

Set your DNS server to 127.0.0.1 or, if you have ipv6, set ipv6 dns to ::1.

If you see your console have DNS resolving outputs, then it can be used normally.


## FAQS

Q: I don't need or have an IPV6 environment, can I turn ipv6 off?

A: Sure. Open `config.py`, set `enable_ipv6` to `False`.

Q: Where can I find suitable cloudflare ips?

A: You can go here: https://github.com/XIU2/CloudflareSpeedTest.

## Thanks to:

*  https://github.com/XIU2/CloudflareSpeedTest

*  https://github.com/zhengxiaowai/tcping , Modified code for ipv6 tcping

## Caution:

This project is for educational use only. Do not use this item for any related activities that violate the laws of your region.

If you do not comply with the above terms, any consequences will be borne by you. The author assumes no responsibility.