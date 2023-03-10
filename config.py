from dnserver import DNSServer,Zone
TTL = 20 # The sleep time (seconds) for each tcping test.
tcping_times = 3 # Set the tcping times you want to.
tcping_success_times = 2 # Must be NO MORE THAN tcping_times.
pause_times_no_ip = 10 # Set when ip is failing to connect,
                       # how many times will it pause to find a new ip.
ttl_interval_add = 20 # Set when after a success checking, how many seconds will the sleep timer add.
check_thread = 30 # Set checking thread while failing.
server = DNSServer(port=53,upstream='192.168.31.1')
enable_ipv6 = True
domain_list = ['osu.ppy.sh','bm4.ppy.sh','bm5.ppy.sh','bm6.ppy.sh','bm7.ppy.sh','bm8.ppy.sh','assets.ppy.sh','m1.ppy.sh','m2.ppy.sh','m3.ppy.sh','c1.ppy.sh','c2.ppy.sh','c3.ppy.sh','c4.ppy.sh','c5.ppy.sh','c6.ppy.sh','a.ppy.sh','b.ppy.sh','c.ppy.sh','i.ppy.sh','osusig.ppy.sh','ppy.sh','osx.ppy.sh','old.ppy.sh','status.ppy.sh','s.ppy.sh','w.ppy.sh','osustats.ppy.sh','next.ppy.sh','news.ppy.sh','stat.ppy.sh','forum-files.ppy.sh','form-auth.ppy.sh','www.osustats.ppy.sh','mini-assets.ppy.sh','spectator2.ppy.sh','notify.ppy.sh','ws.ppy.sh','tourney.ppy.sh','blog.ppy.sh','send.ppy.sh','smtp.ppy.sh','ce.ppy.sh','www.stat.ppy.sh','pe.ppy.sh','ct.ppy.sh','data.ppy.sh','irc.ppy.sh','spectator.ppy.sh','www.ppy.sh','new.ppy.sh','store.ppy.sh','docs.ppy.sh','nono.ppy.sh','mail.ppy.sh','cho.ppy.sh','help.ppy.sh','merch.ppy.sh','bm10.ppy.sh','bm-temp.ppy.sh','www.osusig.ppy.sh','www.osu.ppy.sh','up.ppy.sh','dev.ppy.sh','oto.ppy.sh','ipv6.ppy.sh','comments.ppy.sh']
