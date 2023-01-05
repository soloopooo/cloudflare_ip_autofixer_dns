## Cloudflare ip 自动更换助手 -- dns

一个运行在本地的DNS服务器，帮助你摆脱运营商对 cloudflare 的阻断，更可以实现负载均衡。

理论上，也可以用于其他 CDN 。自己试试吧！

## 我需要什么？

首先安装 python 3.11.0.

终端中运行 `pip install -r requirements.txt`。

打开 `config.py`。你可以在此进行编辑。

IP 地址池在文件夹 `./file/` 中。

运行 `python3 dns.py`。

把你的 DNS 服务器设定为 127.0.0.1，如果你拥有 ipv6，同时将 ipv6 的服务器设定为 ::1。

设置完毕后如果你看到你的终端中有 DNS 查询记录，就可以正常使用了。


## 问题

Q: 我没有 IPV6 环境，能否关闭？

A: 可以。 打开 `config.py`, 将 `enable_ipv6` 设置为 `False`.

Q: 我在哪里可以找到适合我的 cloudflare 地址池？

A: 去这里试试吧: https://github.com/XIU2/CloudflareSpeedTest.

## 感谢:

*  https://github.com/XIU2/CloudflareSpeedTest

*  https://github.com/zhengxiaowai/tcping , 修改代码支持 ipv6 测试。

## 注意：

本项目仅供学习使用。不得将本项目用于任何违反您所在地区的法律的相关活动。

如果您不遵守以上条款，任何后果将由您承担。作者不负任何责任。