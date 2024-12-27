# Setup Files
Run `setup.py` first to create necessary AWS resources
## Host Prep
Install deps
```bash
apt-get install build-essential python3-dev libnetfilter-queue-dev
```
Capture traffic via iptables. Scripts are hardcoded to use queue number 1. 
### Host 1 (client) Iptables
```bash
iptables -I OUTPUT -d 1.2.3.4 (server ip) -j NFQUEUE --queue-num 1
```
### Host 2 (server) Iptables
```bash
iptables -I OUTPUT -d 1.2.3.4 (client ip) -j NFQUEUE --queue-num 1
```

