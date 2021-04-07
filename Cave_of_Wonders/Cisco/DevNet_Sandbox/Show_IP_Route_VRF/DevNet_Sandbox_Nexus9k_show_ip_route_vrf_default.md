
# Show IP Route VRF
| VRF | Address Family | Route | Active | Metric | Route Preference | Source Protocol | Next Hop Number | Next Hop | Outgoing Interface | Updated | Best Unicast Next Hop |
| --- | -------------- | ----- | ------ | ------ | ---------------- | --------------- | --------------- | -------- | ------------------ | ------- | --------------------- |
| default | ipv4 | 172.16.0.1/32 | True | 0 | 0 | direct | 1 | 172.16.0.1 | Loopback1 | 01:12:01 | True |
| default | ipv4 | 172.16.0.1/32 | True | 0 | 0 | direct | 2 | 172.16.0.1 | Loopback1 | 01:12:01 | True |
| default | ipv4 | 172.16.1.0/30 | True | 0 | 0 | direct | 1 | 172.16.1.1 | Ethernet1/5 | 01:11:01 | True |
| default | ipv4 | 172.16.1.1/32 | True | 0 | 0 | local | 1 | 172.16.1.1 | Ethernet1/5 | 01:11:01 | True |