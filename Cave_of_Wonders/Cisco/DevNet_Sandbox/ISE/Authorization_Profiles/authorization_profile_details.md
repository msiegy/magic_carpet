# Authorization Profile Details
| Profile | Description | Access Type | Authorization Profile Type | Profile Name | VLAN Name | Voice Domain Permission | Web Authentication |
| ------- | ----------- | ----------- | -------------------------- | ------------ | --------- | ----------------------- | ------------------ |
| Blackhole_Wireless_Access | Default profile used to block wireless devices. Ensure that you configure a NULL ROUTE ACL on the Wireless LAN Controller. | ACCESS_ACCEPT | SWITCH | Cisco | N/A | N/A | N/A |
| Cisco_IP_Phones | Default profile used for Cisco Phones. | ACCESS_ACCEPT | SWITCH | Cisco | N/A | True | N/A |
| Cisco_Temporal_Onboard | Onboard the device with Cisco temporal agent | ACCESS_ACCEPT | SWITCH | Cisco | N/A | N/A | N/A |
| Cisco_WebAuth | Default Profile used to redirect users to the CWA portal. | ACCESS_ACCEPT | SWITCH | Cisco | N/A | N/A | N/A |
| DenyAccess | Default Profile with access type as Access-Reject | ACCESS_REJECT | SWITCH | N/A | N/A | N/A | N/A |
| NSP_Onboard | Onboard the device with Native Supplicant Provisioning | ACCESS_ACCEPT | SWITCH | Cisco | N/A | N/A | N/A |
| Non_Cisco_IP_Phones | Default Profile used for Non Cisco Phones. | ACCESS_ACCEPT | SWITCH | Cisco | N/A | True | N/A |
| PermitAccess | Default Profile with access type as Access-Accept | ACCESS_ACCEPT | SWITCH | N/A | N/A | N/A | N/A |
| UDN | Default profile used for UPN. | ACCESS_ACCEPT | SWITCH | Cisco | N/A | N/A | N/A |