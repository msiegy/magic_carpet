# ----------------
# Copyright
# ----------------
# Written by John Capobianco, March 2021
# Copyright (c) 2021 John Capobianco

# ----------------
# Python
# ----------------
import os
import sys
import yaml
import time
import json
import shutil
import logging
import requests
from rich import print
from rich.panel import Panel
from rich.text import Text
from pyats import aetest
from pyats import topology
from pyats.log.utils import banner
from jinja2 import Environment, FileSystemLoader
from ascii_art import GREETING, RUNNING, FINISHED

# ----------------
# Get logger for script
# ----------------

log = logging.getLogger(__name__)

# ----------------
# Filetypes 
# ----------------

filetype_loop = ["csv","md","html"]

# ----------------
# Template Directory
# ----------------

template_dir = 'templates/cisco/nxos'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup):
    """Common Setup section"""
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        print(Panel.fit(Text.from_markup(GREETING, justify="center")))
        testbed.connect(learn_hostname=True)

# ----------------
# Test Case #1
# ----------------
class Collect_Information(aetest.Testcase):
    """Parse all the commands"""

    @aetest.test
    def parse(self, testbed, section, steps):
        """ Testcase Setup section """
        # ---------------------------------------
        # Loop over devices
        # ---------------------------------------
        for device in testbed:
            # ---------------------------------------
            # Execute parser for various show commands
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(RUNNING, justify="center")))

            # Show Access-Lists
            with steps.start('Parsing show access-lists',continue_=True) as step:
                try:
                    self.parsed_show_access_lists = device.parse("show access-lists")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # show bgp process vrf all
            with steps.start('Parsing show bgp process vrf all',continue_=True) as step:
                try:
                    self.parsed_show_bgp_process_vrf_all = device.parse("show bgp process vrf all")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show BGP Sessions
            with steps.start('Parsing show bgp sessions',continue_=True) as step:
                try:
                    self.parsed_show_bgp_sessions = device.parse("show bgp sessions")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Interfaces Status
            with steps.start('Parsing show interface status',continue_=True) as step:
                try:
                    self.parsed_show_int_status = device.parse("show interface status")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Inventory
            with steps.start('Parsing show inventory',continue_=True) as step:
                try:
                    self.parsed_show_inventory = device.parse("show inventory")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show IP Interface Brief
            with steps.start('Parsing show ip interface brief',continue_=True) as step:
                try:
                    self.parsed_show_ip_int_brief = device.parse("show ip interface brief")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show IP OSPF Layer 3 Command only 
            with steps.start('Parsing show ip ospf',continue_=True) as step:
                try:
                    self.parsed_show_ip_ospf = device.parse("show ip ospf")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show IP Route - Layer 3 Command Only
            with steps.start('Parsing show ip route',continue_=True) as step:
                try:
                    self.parsed_show_ip_route = device.parse("show ip route")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show MAC Address-Table
            with steps.start('Parsing show mac address-table',continue_=True) as step:
                try:
                    self.parsed_show_mac_address_table = device.parse("show mac address-table")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Portchannel Summary
            with steps.start('Parsing show port-channel summary',continue_=True) as step:
                try:
                    self.parsed_show_port_channel_summary = device.parse("show port-channel summary")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Version
            with steps.start('Parsing show version',continue_=True) as step:
                try:
                    self.parsed_show_version = device.parse("show version")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show VLAN
            with steps.start('Parsing show vlan',continue_=True) as step:
                try:
                    self.parsed_show_vlan = device.parse("show vlan")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show VRF - Layer 3 Command only 
            with steps.start('Parsing show vrf',continue_=True) as step:
                try:
                    self.parsed_show_vrf = device.parse("show vrf")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # show vrf all detail - Layer 3 Command only 
            with steps.start('Parsing show vrf all detail',continue_=True) as step:
                try:
                    self.parsed_show_vrf_all_detail = device.parse("show vrf all detail")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # show vrf all interface - Layer 3 Command only 
            with steps.start('Parsing show vrf all interface',continue_=True) as step:
                try:
                    self.parsed_show_vrf_all_interface = device.parse("show vrf all interface")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # ---------------------------------------
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed Data
            # ---------------------------------------         
            
            with steps.start('Store data',continue_=True) as step:

                # Show access-lists
                if hasattr(self, 'parsed_show_access_lists'):
                    sh_access_lists_template = env.get_template('show_access_lists.j2')                  

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_access_lists, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_access_lists, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_access_lists_template.render(to_parse_access_list=self.parsed_show_access_lists,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists_mind_map.html" % (device.alias,device.alias))

                # Show BGP process vrf all
                if hasattr(self, 'parsed_show_bgp_process_vrf_all'):
                    sh_bgp_process_vrf_all_template = env.get_template('show_bgp_process_vrf_all.j2')                  
                    sh_bgp_process_vrf_all_netjson_json_template = env.get_template('show_bgp_process_vrf_all_netjson_json.j2')
                    sh_bgp_process_vrf_all_netjson_html_template = env.get_template('show_bgp_process_vrf_all_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_bgp_process_vrf_all, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_bgp_process_vrf_all, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_bgp_process_vrf_all_template.render(to_parse_bgp=self.parsed_show_bgp_process_vrf_all,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_bgp_process_vrf_all_netjson_json_template.render(to_parse_bgp=self.parsed_show_bgp_process_vrf_all,device_alias = device.alias)
                    parsed_output_netjson_html = sh_bgp_process_vrf_all_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                # Show BGP Sessions
                if hasattr(self, 'parsed_show_bgp_sessions'):
                    sh_bgp_sessions_template = env.get_template('show_bgp_sessions.j2')                  
                    sh_bgp_sessions_netjson_json_template = env.get_template('show_bgp_sessions_netjson_json.j2')
                    sh_bgp_sessions_netjson_html_template = env.get_template('show_bgp_sessions_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_bgp_sessions, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_bgp_sessions, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_bgp_sessions_template.render(to_parse_bgp=self.parsed_show_bgp_sessions,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_bgp_sessions_netjson_json_template.render(to_parse_bgp=self.parsed_show_bgp_sessions)
                    parsed_output_netjson_html = sh_bgp_sessions_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                # Show interface status
                if hasattr(self, 'parsed_show_int_status'):
                    sh_int_status_template = env.get_template('show_int_status.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_int_status, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_int_status, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_int_status_template.render(to_parse_interfaces=self.parsed_show_int_status['interfaces'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)  

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status_mind_map.html" % (device.alias,device.alias))

                # Show Inventory
                if hasattr(self, 'parsed_show_inventory'):
                    # Nexus 
                    sh_inventory_nexus_template = env.get_template('show_inventory_nexus.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_inventory_nexus_template.render(to_parse_inventory_name=self.parsed_show_inventory['name'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)

                        if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory.md" % device.alias):
                            os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                # Show ip interface brief
                if hasattr(self, 'parsed_show_ip_int_brief'):
                    sh_ip_int_brief_template = env.get_template('show_ip_int_brief.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief.json" % device.alias, "w") as fid:
                        json.dump(self.parsed_show_ip_int_brief, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.parsed_show_ip_int_brief, yml, allow_unicode=True)                 
        
                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_int_brief_template.render(to_parse_interfaces=self.parsed_show_ip_int_brief['interface'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief_mind_map.html" % (device.alias,device.alias))

                # Show IP OSPF
                if hasattr(self, 'parsed_show_ip_ospf'):
                    sh_ip_ospf_template = env.get_template('show_ip_ospf.j2')
                    
                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ip_ospf, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ip_ospf, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_template.render(to_parse_ip_ospf=self.parsed_show_ip_ospf['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf_mind_map.html" % (device.alias,device.alias))

                # Show ip Route
                if hasattr(self, 'parsed_show_ip_route'):
                    sh_ip_route_template = env.get_template('show_ip_route.j2')
                    sh_ip_route_netjson_json_template = env.get_template('show_ip_route_netjson_json.j2')
                    sh_ip_route_netjson_html_template = env.get_template('show_ip_route_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ip_route, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ip_route, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_route_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ip_route_netjson_json_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_route_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                # Show mac address-table
                if hasattr(self, 'parsed_show_mac_address_table'):
                    sh_mac_address_table_template = env.get_template('show_mac_address_table.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_mac_address_table, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_mac_address_table, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_mac_address_table_template.render(to_parse_mac_address_table=self.parsed_show_mac_address_table['mac_table'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table_mind_map.html" % (device.alias,device.alias))

                # Show port-channel summary
                if hasattr(self, 'parsed_show_port_channel_summary'):
                    sh_portchannel_summary_template = env.get_template('show_portchannel_summary.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_port_channel_summary, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_port_channel_summary, yml, allow_unicode=True)

                    for filetype in filetype_loop:                       
                        parsed_output_type = sh_portchannel_summary_template.render(to_parse_etherchannel_summary=self.parsed_show_port_channel_summary['interfaces'],filetype_loop_jinja2=filetype)
                      
                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary_mind_map.html" % (device.alias,device.alias))

                # Show version
                if hasattr(self, 'parsed_show_version'):
                    sh_ver_template = env.get_template('show_version.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_version, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_version, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ver_template.render(to_parse_version=self.parsed_show_version['platform'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version_mind_map.html" % (device.alias,device.alias))

                # Show vrf
                if hasattr(self, 'parsed_show_vrf'):
                    sh_vrf_template = env.get_template('show_vrf.j2')
                    sh_ip_arp_vrf_template = env.get_template('show_ip_arp_vrf.j2')
                    sh_ip_arp_vrf_stats_template = env.get_template('show_ip_arp_vrf_statistics.j2')
                    sh_ip_route_template = env.get_template('show_ip_route_vrf.j2')
                    
                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_vrf, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_vrf, yml, allow_unicode=True)

                    for filetype in filetype_loop:      
                        parsed_output_type = sh_vrf_template.render(to_parse_vrf=self.parsed_show_vrf['vrfs'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf_mind_map.html" % (device.alias,device.alias))

                # Show vrf all detail
                if hasattr(self, 'parsed_show_vrf_all_detail'):
                    sh_vrf_all_detail_template = env.get_template('show_vrf_all_detail.j2')
                    
                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_vrf_all_detail, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_vrf_all_detail, yml, allow_unicode=True)

                    for filetype in filetype_loop:      
                        parsed_output_type = sh_vrf_all_detail_template.render(to_parse_vrf=self.parsed_show_vrf_all_detail,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail_mind_map.html" % (device.alias,device.alias))

                # Show vrf all interface
                if hasattr(self, 'parsed_show_vrf_all_interface'):
                    sh_vrf_all_interface_template = env.get_template('show_vrf_all_interface.j2')
                    
                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_vrf_all_interface, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_vrf_all_interface, yml, allow_unicode=True)

                    for filetype in filetype_loop:      
                        parsed_output_type = sh_vrf_all_interface_template.render(to_parse_vrf=self.parsed_show_vrf_all_interface,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface_mind_map.html" % (device.alias,device.alias))

                # Show vlan
                if hasattr(self, 'parsed_show_vlan'):
                    sh_vlan_template = env.get_template('show_vlan.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_vlan, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_vlan, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_vlan_template.render(to_parse_vlan=self.parsed_show_vlan['vlans'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan_mind_map.html" % (device.alias,device.alias))

                    # For Each VRF
                    for vrf in self.parsed_show_vrf['vrfs']:

                        # Show IP ARP VRF <VRF> 
                        with steps.start('Parsing ip arp vrf',continue_=True) as step:
                            try:
                                self.parsed_show_ip_arp_vrf = device.parse("show ip arp vrf %s" % vrf)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))

                        with steps.start('Store data',continue_=True) as step:

                            with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                json.dump(self.parsed_show_ip_arp_vrf, fid, indent=4, sort_keys=True)

                            with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                yaml.dump(self.parsed_show_ip_arp_vrf, yml, allow_unicode=True)

                            for filetype in filetype_loop:
                                parsed_output_type = sh_ip_arp_vrf_template.render(to_parse_ip_arp=self.parsed_show_ip_arp_vrf['interfaces'],filetype_loop_jinja2=filetype)

                                with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                    fh.write(parsed_output_type)
        
                            if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.md" % (device.alias,vrf)):
                                os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                            for filetype in filetype_loop:
                                parsed_output_type = sh_ip_arp_vrf_stats_template.render(to_parse_ip_arp=self.parsed_show_ip_arp_vrf['statistics'],filetype_loop_jinja2=filetype)

                                with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_statistics_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                    fh.write(parsed_output_type)
        
                            if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_statistics_%s.md" % (device.alias,vrf)):
                                os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_statistics_%s.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_statistics_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                            # Show IP ROUTE VRF <VRF> 
                            with steps.start('Parsing ip route vrf',continue_=True) as step:
                                try:
                                    self.parsed_show_ip_route_vrf = device.parse("show ip route vrf %s" % vrf)
                                except Exception as e:
                                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

                            with steps.start('Store data',continue_=True) as step:

                                with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                  json.dump(self.parsed_show_ip_route_vrf, fid, indent=4, sort_keys=True)

                                with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                  yaml.dump(self.parsed_show_ip_route_vrf, yml, allow_unicode=True)
                         
                                for filetype in filetype_loop:
                                    parsed_output_type = sh_ip_route_template.render(to_parse_ip_route=self.parsed_show_ip_route_vrf['vrf'],filetype_loop_jinja2=filetype)

                                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                      fh.write(parsed_output_type)

                                if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.md" % (device.alias,vrf)):
                                    os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))


        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED, justify="center")))            