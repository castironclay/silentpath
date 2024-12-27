# Setup Files
Run `setup_files/setup.py` first to create necessary AWS resources
## Host Prep
Install deps
```bash
apt-get install build-essential python3-dev libnetfilter-queue-dev
```
Capture traffic via iptables. Scripts are hardcoded to use queue number 1. 
### Host 1 (server) Iptables
```bash
# This iptables rule can be fine tuned to specific port/protocols
# How it is written below will capture all traffic
iptables -I OUTPUT -d 1.2.3.4 (client ip) -j NFQUEUE --queue-num 1
# Pulls messages from SQS queue
python sqs_server_listener.py
# Grabs messages from nfqueue and sends to SQS
python sqs_server_to_client_send.py
```
### Host 2 (cient) Iptables
```bash
# This iptables rule can be fine tuned to specific port/protocols
# How it is written below will capture all traffic
iptables -I OUTPUT -d 1.2.3.4 (server ip) -j NFQUEUE --queue-num 1
# Pulls messages from SQS queue
python sqs_client_listener.py
# Grabs messages from nfqueue and sends to SQS
python sqs_client_to_server_send.py
```
## Set Interface name
Set name of destination interface on line `18` of listener scripts. This is needed to capture the mac as the destination of Scapy sendp for the receiving host. 
# TODOs
- support other paths
- add/remove iptables rules upon script start/stop
- args for interface name
- start listener and sender in same script