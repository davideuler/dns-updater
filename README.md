Put the ak/sk, and domain name to update in config.py

```
aliyun_ak=""
aliyun_sk=""
domain = 'mydomain.com'
name_ipv4 = "subdomain"
name_ipv6 = "www"

```

Then run the dns updater every 5 minutes:
```
watch -n 300 python3 update_dns.py
```
