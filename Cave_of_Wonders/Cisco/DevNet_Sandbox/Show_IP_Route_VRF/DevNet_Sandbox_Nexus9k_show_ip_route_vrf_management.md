
# Show IP Route (Global Routing Table)
| VRF | Address Family | Route | Active | Metric | Route Preference | Source Protocol | Source Protocol Code | Next Hop Number | Next Hop | Outgoing Interface | Updated |
| --- | -------------- | ----- | ------ | ------ | ---------------- | --------------- | -------------------- | --------------- | -------- | ------------------ | ------- |
| management | ipv4 | 0.0.0.0/0 | True | 0 | 1 | static |  | 1 | 10.10.20.254 |  | 00:52:51 |
| management | ipv4 | 10.10.20.0/24 | True | 0 | 0 | direct |  | 1 | 10.10.20.58 | mgmt0 | 00:52:51 |
| management | ipv4 | 10.10.20.58/32 | True | 0 | 0 | local |  | 1 | 10.10.20.58 | mgmt0 | 00:52:51 |