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
from ascii_art import GREETING, LEARN, RUNNING, FINISHED

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

template_dir = 'templates/cisco/ios_xe'
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
        testbed.connect()

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
            # Genie learn().info for various functions
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(LEARN, justify="center")))

            # ACLs
            with steps.start('Learning Access Lists',continue_=True) as step:
                try:
                    self.learned_acl = device.learn('acl').info
                except Exception as e:
                    step.failed('Could not learn ACL\n{e}'.format(e=e))

            # ARP
            with steps.start('Learning ARP',continue_=True) as step:
                try:
                    self.learned_arp = device.learn('arp').info
                except Exception as e:
                    step.failed('Could not learn ARP\n{e}'.format(e=e))

            # Interface
            with steps.start('Learning Interface',continue_=True) as step:
                try:
                    self.learned_interface = device.learn('interface').info
                except Exception as e:
                    step.failed('Could not learn Interface\n{e}'.format(e=e))

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

            # Show Access-Sessions
            if device.type == "switch":            
                with steps.start('Parsing show access-session',continue_=True) as step:
                    try:
                        self.parsed_show_access_session = device.parse("show access-session")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Authentication Sessions
            if device.type == "switch":            
                with steps.start('Parsing show authentication sessions',continue_=True) as step:
                    try:
                        self.parsed_show_authentication_sessions = device.parse("show authentication sessions")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show CDP Neighbors
            with steps.start('Parsing show cdp neighbors',continue_=True) as step:
                try:
                    self.parsed_show_cdp_neighbors = device.parse("show cdp neighbors")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show CDP Neighbors Detail           
            with steps.start('Parsing show cdp neighbors detail',continue_=True) as step:
                try:
                    self.parsed_show_cdp_neighbors_detail = device.parse("show cdp neighbors detail")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Enviroment
            with steps.start('Parsing show environment all',continue_=True) as step:
                try:
                    self.parsed_show_environment = device.parse("show environment all")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Etherchannel Summary
            with steps.start('Parsing show etherchannel summary',continue_=True) as step:
                try:
                    self.parsed_show_etherchannel_summary = device.parse("show etherchannel summary")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Interfaces
            with steps.start('Parsing show interfaces',continue_=True) as step:
                try:
                    self.parsed_show_int = device.parse("show interfaces")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Interfaces Status
            with steps.start('Parsing show interfaces status',continue_=True) as step:
                try:
                    self.parsed_show_int_status = device.parse("show interfaces status")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Interfaces Trunk
            with steps.start('Parsing show interfaces trunk',continue_=True) as step:
                try:
                    self.parsed_show_interfaces_trunk = device.parse("show interfaces trunk")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Inventory
            with steps.start('Parsing show inventory',continue_=True) as step:
                try:
                    self.parsed_show_inventory = device.parse("show inventory")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show IP ARP - Layer 3 Command only 
            # Test if device.type == "router"
            if device.type == "router":            
                with steps.start('Parsing show ip arp',continue_=True) as step:
                    try:
                        self.parsed_show_ip_arp = device.parse("show ip arp")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show IP Interface Brief
            with steps.start('Parsing show ip interface brief',continue_=True) as step:
                try:
                    self.parsed_show_ip_int_brief = device.parse("show ip interface brief")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show IP OSPF Layer 3 Command only 
            # Test if device.type == "router"
            if device.type == "router":
                with steps.start('Parsing show ip ospf',continue_=True) as step:
                    try:
                        self.parsed_show_ip_ospf = device.parse("show ip ospf")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show IP OSPF Dabase Layer 3 Command only 
            # Test if device.type == "router"
            if device.type == "router":
                with steps.start('Parsing show ip ospf database',continue_=True) as step:
                    try:
                        self.parsed_show_ip_ospf_database = device.parse("show ip ospf database")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show IP OSPF Interface Layer 3 Command only 
            # Test if device.type == "router"
            if device.type == "router":
                with steps.start('Parsing show ip ospf interface',continue_=True) as step:
                    try:
                        self.parsed_show_ip_ospf_interface = device.parse("show ip ospf interface")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show IP OSPF Neighbor - Layer 3 Command only 
            # Test if device.type == "router"
            if device.type == "router":
                with steps.start('Parsing show ip ospf neighbor',continue_=True) as step:
                    try:
                        self.parsed_show_ip_ospf_neighbor = device.parse("show ip ospf neighbor")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show IP OSPF Neighbor Detail - Layer 3 Command only 
            # Test if device.type == "router"
            if device.type == "router":
                with steps.start('Parsing show ip ospf neighbor detail',continue_=True) as step:
                    try:
                        self.parsed_show_ip_ospf_neighbor_detail = device.parse("show ip ospf neighbor detail")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show IP Route - Layer 3 Command Only
            if device.type == "router":
                with steps.start('Parsing show ip route',continue_=True) as step:
                    try:
                        self.parsed_show_ip_route = device.parse("show ip route")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show ISSU State Detail
            ## Only VSS Systems support ISSU Such as a 4500; test if device.platform == 4500
            if device.platform == "cat4500":
                with steps.start('Parsing show issu state detail',continue_=True) as step:
                    try:
                        self.parsed_show_issu_state = device.parse("show issu state detail")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show MAC Address-Table
            with steps.start('Parsing show mac address-table',continue_=True) as step:
                try:
                    self.parsed_show_mac_address_table = device.parse("show mac address-table")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show NTP Associations
            with steps.start('Parsing show ntp associations',continue_=True) as step:
                try:
                    self.parsed_show_ntp_associations = device.parse("show ntp associations")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Power Inline
            if device.type == "switch":
                with steps.start('Parsing show power inline',continue_=True) as step:
                    try:
                        self.parsed_show_power_inline = device.parse("show power inline")
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
            # Test if device.type == "router"
            if device.type == "router":            
                with steps.start('Parsing show vrf',continue_=True) as step:
                    try:
                        self.parsed_show_vrf = device.parse("show vrf")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # ---------------------------------------
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed Data
            # ---------------------------------------         
            
            with steps.start('Store data',continue_=True) as step:

                ###############################
                # Genie learn().info section
                ###############################

                # Learned ACL
                if hasattr(self, 'learned_acl'):
                    learned_acl_template = env.get_template('learned_acl.j2')
                    learned_acl_netjson_json_template = env.get_template('learned_acl_netjson_json.j2')
                    learned_acl_netjson_html_template = env.get_template('learned_acl_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ACL/%s_learned_acl.json" % device.alias, "w") as fid:
                        json.dump(self.learned_acl, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ACL/%s_learned_acl.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.learned_acl, yml, allow_unicode=True)                

                    for filetype in filetype_loop:
                        parsed_output_type = learned_acl_template.render(to_parse_access_list=self.learned_acl['acls'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ACL/%s_learned_acl.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Learned_ACL/%s_learned_acl.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Learned_ACL/%s_learned_acl.md --output Cave_of_Wonders/Cisco/IOS_XE/Learned_ACL/%s_learned_acl_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_acl_netjson_json_template.render(to_parse_access_list=self.learned_acl['acls'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_acl_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ACL/%s_learned_acl_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ACL/%s_learned_acl_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                # Learned ARP
                if hasattr(self, 'learned_arp'):
                    learned_arp_template = env.get_template('learned_arp.j2')
                    learned_arp_statistics_template = env.get_template('learned_arp_statistics.j2')
                    learned_arp_netjson_json_template = env.get_template('learned_arp_netjson_json.j2')
                    learned_arp_netjson_html_template = env.get_template('learned_arp_netjson_html.j2')
                    learned_arp_statistics_netjson_json_template = env.get_template('learned_arp_statistics_netjson_json.j2')
                    learned_arp_statistics_netjson_html_template = env.get_template('learned_arp_statistics_netjson_html.j2')


                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp.json" % device.alias, "w") as fid:
                        json.dump(self.learned_arp, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.learned_arp, yml, allow_unicode=True)   

                    for filetype in filetype_loop:
                        parsed_output_type = learned_arp_template.render(to_parse_arp=self.learned_arp['interfaces'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 

                    for filetype in filetype_loop:
                        parsed_output_type = learned_arp_statistics_template.render(to_parse_arp=self.learned_arp['statistics'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_statistics.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp.md --output Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_statistics.md --output Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_statistics_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_arp_netjson_json_template.render(to_parse_arp=self.learned_arp['interfaces'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_arp_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    parsed_output_netjson_json = learned_arp_statistics_netjson_json_template.render(to_parse_arp=self.learned_arp['statistics'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_arp_statistics_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_statistics_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_statistics_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                # Show access-lists
                if hasattr(self, 'parsed_show_access_lists'):
                    sh_access_lists_template = env.get_template('show_access_lists.j2')                  

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_access_lists, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_access_lists, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_access_lists_template.render(to_parse_access_list=self.parsed_show_access_lists,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists_mind_map.html" % (device.alias,device.alias))

                # Learned Interface
                if hasattr(self, 'learned_interface'):
                    learned_interface_template = env.get_template('learned_interface.j2')
                    learned_interface_netjson_json_template = env.get_template('learned_interface_netjson_json.j2')
                    learned_interface_netjson_html_template = env.get_template('learned_interface_netjson_html.j2')
                    learned_interface_enable_netjson_json_template = env.get_template('learned_interface_enabled_netjson_json.j2')
                    learned_interface_enable_netjson_html_template = env.get_template('learned_interface_enabled_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_Interface/%s_learned_interface.json" % device.alias, "w") as fid:
                        json.dump(self.learned_interface, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_Interface/%s_learned_interface.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.learned_interface, yml, allow_unicode=True)   

                    for filetype in filetype_loop:
                        parsed_output_type = learned_interface_template.render(to_parse_interface=self.learned_interface,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_Interface/%s_learned_interface.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Learned_Interface/%s_learned_interface.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Learned_Interface/%s_learned_interface.md --output Cave_of_Wonders/Cisco/IOS_XE/Learned_Interface/%s_learned_interface_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_interface_netjson_json_template.render(to_parse_interface=self.learned_interface,device_alias = device.alias)
                    parsed_output_netjson_html = learned_interface_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_Interface/%s_learned_interface_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_Interface/%s_learned_interface_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    parsed_output_netjson_json = learned_interface_enable_netjson_json_template.render(to_parse_interface=self.learned_interface,device_alias = device.alias)
                    parsed_output_netjson_html = learned_interface_enable_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_Interface/%s_learned_interface_enabled_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Learned_Interface/%s_learned_interface_enabled_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                ###############################
                # Genie Show Command Section
                ###############################

                # Show access-session
                if hasattr(self, 'parsed_show_access_session'):
                    sh_access_sessions_template = env.get_template('show_access_sessions.j2')
                    sh_access_sessions_totals_template = env.get_template('show_access_sessions_totals.j2')
                    sh_access_sessions_interface_details_template = env.get_template('show_access_sessions_interface_details.j2')
                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.json" % (device.alias)):
                       os.remove("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.json" % (device.alias))

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.yaml" % (device.alias)):
                       os.remove("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.yaml" % (device.alias))

                    for filetype in filetype_loop:
                        if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.%s" % (device.alias,filetype)):
                            os.remove("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.%s" % (device.alias,filetype))

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.csv" % device.alias,'a') as csv:
                        csv.seek(0, 0)
                        csv.write("Interface,User Name,Mac Address,Current Policy,Domain,IPv4 Address,IPv6 Address,VLAN,Method,State,Host Mode,Session Timeout Remaining,Status")
                    csv.close()                                   

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.md" % device.alias,'a') as md:
                        md.seek(0, 0)
                        md.write("# Show Access-Session Interface Details")
                        md.write("\n")
                        md.write("| Interface | User Name | Mac Address | Current Policy | Domain | IPv4 Address | IPv6 Address | VLAN | Method | State | Host Mode | Session Timeout Remaining | Status |")
                        md.write("\n")
                        md.write("| --------- | --------- | ----------- | -------------- | ------ | ------------ | ------------ | ---- | ------ | ----- | --------- | ------------------------- | ------ |")
                    md.close() 

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.html" % device.alias,'a') as html:
                        html.seek(0, 0)
                        html.write("<html><body><h1>Show Access Sessions</h1><table style=\"width:100%\">")
                        html.write("\n")
                        html.write("<tr><th>Interface</th><th>User Name</th><th>MAC Address</th><th>Current Policy</th><th>Domain</th><th>IPv4 Address</th><th>IPv6 Address</th><th>VLAN</th><th>Method</th><th>State</th><th>Host Mode</th><th>Session Timeout Remaining</th><th>Status</th></tr>")                     
                    html.close() 

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_access_session, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_access_session, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_access_sessions_template.render(to_parse_access_session=self.parsed_show_access_session['interfaces'],filetype_loop_jinja2=filetype)
                        parsed_output_totals_type = sh_access_sessions_totals_template.render(to_parse_access_session=self.parsed_show_access_session,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session_totals.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_totals_type) 

                    # Show access-session interface <int> details
                    for interface in self.parsed_show_access_session['interfaces']:
                        with steps.start('Parsing show access-session interface details',continue_=True) as step:
                            try:
                                self.parsed_show_ip_access_session_interface_details = device.parse("show access-session interface %s details" % interface)

                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))

                        with steps.start('Store data',continue_=True) as step:       
                            with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.json" % (device.alias), "a") as fid:
                                json.dump(self.parsed_show_ip_access_session_interface_details, fid, indent=4, sort_keys=True)
                                fid.write('\n')
                                
                            with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.yaml" % (device.alias), "a") as yml:
                                yaml.dump(self.parsed_show_ip_access_session_interface_details, yml, allow_unicode=True)
                         
                            for filetype in filetype_loop:
                                parsed_output_type = sh_access_sessions_interface_details_template.render(to_parse_access_interface_details=self.parsed_show_ip_access_session_interface_details['interfaces'],filetype_loop_jinja2=filetype)

                                with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.%s" % (device.alias,filetype), "a") as fh:
                                    fh.write(parsed_output_type)

                            fh.close()

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.html" % device.alias,'a') as html:
                        html.write("</table></body></html>")
                    html.close() 
                                    
                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details_mind_map.html" % (device.alias,device.alias))

                    fid.close()
                    yml.close()

                if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session.md" % device.alias):
                    os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session_mind_map.html" % (device.alias,device.alias))

                if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session_totals.md" % device.alias):
                    os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session_totals.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session_totals_mind_map.html" % (device.alias,device.alias))

                # Show Authentication Sessions
                if hasattr(self, 'parsed_show_authentication_sessions'):
                    sh_authetication_sessions_template = env.get_template('show_authentication_sessions.j2')
                    sh_authetication_sessions_totals_template = env.get_template('show_authentication_sessions_totals.j2')
                    sh_authentication_sessions_interface_details_template = env.get_template('show_authentication_sessions_interface_details.j2')
                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.json" % (device.alias)):
                       os.remove("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.json" % (device.alias))

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.yaml" % (device.alias)):
                       os.remove("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.yaml" % (device.alias))

                    for filetype in filetype_loop:
                        if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.%s" % (device.alias,filetype)):
                            os.remove("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.%s" % (device.alias,filetype))

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.csv" % device.alias,'a') as csv:
                        csv.seek(0, 0)
                        csv.write("Interface,User Name,Mac Address,Current Policy,Domain,IPv4 Address,IPv6 Address,VLAN,Method,State,Host Mode,Session Timeout Remaining,Status")
                    csv.close()                                   

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.md" % device.alias,'a') as md:
                        md.seek(0, 0)
                        md.write("# Show Authentication Session Interface Details")
                        md.write("\n")
                        md.write("| Interface | User Name | Mac Address | Current Policy | Domain | IPv4 Address | IPv6 Address | VLAN | Method | State | Host Mode | Session Timeout Remaining | Status |")
                        md.write("\n")
                        md.write("| --------- | --------- | ----------- | -------------- | ------ | ------------ | ------------ | ---- | ------ | ----- | --------- | ------------------------- | ------ |")
                    md.close() 

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.html" % device.alias,'a') as html:
                        html.seek(0, 0)
                        html.write("<html><body><h1>Show Authentication Sessions</h1><table style=\"width:100%\">")
                        html.write("\n")
                        html.write("<tr><th>Interface</th><th>User Name</th><th>MAC Address</th><th>Current Policy</th><th>Domain</th><th>IPv4 Address</th><th>IPv6 Address</th><th>VLAN</th><th>Method</th><th>State</th><th>Host Mode</th><th>Session Timeout Remaining</th><th>Status</th></tr>")                     
                    html.close()

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_authentication_sessions, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_authentication_sessions, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_authetication_sessions_template.render(to_parse_authentication_sessions=self.parsed_show_authentication_sessions['interfaces'],filetype_loop_jinja2=filetype)
                        parsed_output_totals_type = sh_authetication_sessions_totals_template.render(to_parse_authentication_sessions=self.parsed_show_authentication_sessions,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_session_totals.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 

                    # Show authentication session interface <int> details
                    for interface in self.parsed_show_authentication_sessions['interfaces']:
                        with steps.start('Parsing show authentication session interface details',continue_=True) as step:
                            try:
                                self.parsed_show_authentication_session_interface_details = device.parse("show authentication sessions interface %s details" % interface)

                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))

                        with steps.start('Store data',continue_=True) as step:       
                            with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.json" % (device.alias), "a") as fid:
                                json.dump(self.parsed_show_authentication_session_interface_details, fid, indent=4, sort_keys=True)
                                fid.write('\n')
                                
                            with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.yaml" % (device.alias), "a") as yml:
                                yaml.dump(self.parsed_show_authentication_session_interface_details, yml, allow_unicode=True)
                         
                            for filetype in filetype_loop:
                                parsed_output_type = sh_authentication_sessions_interface_details_template.render(to_parse_access_interface_details=self.parsed_show_authentication_session_interface_details['interfaces'],filetype_loop_jinja2=filetype)

                                with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.%s" % (device.alias,filetype), "a") as fh:
                                    fh.write(parsed_output_type)

                            fh.close()

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.html" % device.alias,'a') as html:
                        html.write("</table></body></html>")
                    html.close() 
                                    
                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details_mind_map.html" % (device.alias,device.alias))

                    fid.close()
                    yml.close()

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_session_totals.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_session_totals.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_session_totals_mind_map.html" % (device.alias,device.alias))

                # Show CDP Neighbors
                if hasattr(self, 'parsed_show_cdp_neighbors'):
                    sh_cdp_neighbors_template = env.get_template('show_cdp_neighbors.j2')
                    sh_cdp_neighbors_netjson_json_template = env.get_template('show_cdp_neighbor_netjson_json.j2')
                    sh_cdp_neighbors_netjson_html_template = env.get_template('show_cdp_neighbor_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_cdp_neighbors, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_cdp_neighbors, yml, allow_unicode=True)

                    for filetype in filetype_loop:                    
                        parsed_output_type = sh_cdp_neighbors_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors['cdp'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)  
                                       
                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_cdp_neighbors_netjson_json_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors['cdp'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_cdp_neighbors_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                # Show CDP Neighbors Details
                if hasattr(self, 'parsed_show_cdp_neighbors_detail'):
                    sh_cdp_neighbors_detail_template = env.get_template('show_cdp_neighbors_details.j2')
                    sh_cdp_neighbors_detail_totals_template = env.get_template('show_cdp_neighbors_details_totals.j2')
                    sh_cdp_neighbors_detail_netjson_json_template = env.get_template('show_cdp_neighbor_details_netjson_json.j2')
                    sh_cdp_neighbors_detail_netjson_html_template = env.get_template('show_cdp_neighbor_details_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_cdp_neighbors_detail, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_cdp_neighbors_detail, yml, allow_unicode=True)

                    for filetype in filetype_loop:                    
                        parsed_output_type = sh_cdp_neighbors_detail_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors_detail['index'],filetype_loop_jinja2=filetype)
                        parsed_totals = sh_cdp_neighbors_detail_totals_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors_detail,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)               

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_totals.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_totals)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_detail_totals.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_totals.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_totals_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_cdp_neighbors_detail_netjson_json_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors_detail['index'],filetype_loop_jinja2=filetype,device_ip = device.connections.cli.ip)
                    parsed_output_netjson_html = sh_cdp_neighbors_detail_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                # Show environment all
                if hasattr(self, 'parsed_show_environment'):
                    sh_environment_template = env.get_template('show_environment_all.j2')
                    
                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Environment/%s_show_environment.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_environment, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Environment/%s_show_environment.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_environment, yml, allow_unicode=True)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_environment_template.render(to_parse_environment=self.parsed_show_environment['switch'],filetype_loop_jinja2=filetype)
                      
                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Environment/%s_show_environment.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Environment/%s_show_environment.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Environment/%s_show_environment.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Environment/%s_show_environment_mind_map.html" % (device.alias,device.alias))

                # Show etherchannel summary
                if hasattr(self, 'parsed_show_etherchannel_summary'):
                    sh_etherchannel_summary_template = env.get_template('show_etherchannel_summary.j2')
                    sh_etherchannel_summary_totals_template = env.get_template('show_etherchannel_summary_totals.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_etherchannel_summary, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_etherchannel_summary, yml, allow_unicode=True)

                    for filetype in filetype_loop: 
                        if 'interfaces' in self.parsed_show_etherchannel_summary:                          
                            parsed_output_type = sh_etherchannel_summary_template.render(to_parse_etherchannel_summary=self.parsed_show_etherchannel_summary['interfaces'],filetype_loop_jinja2=filetype)
                        parsed_totals = sh_etherchannel_summary_totals_template.render(to_parse_etherchannel_summary=self.parsed_show_etherchannel_summary,filetype_loop_jinja2=filetype)
                      
                        if parsed_output_type in locals():                                                    
                            with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary.%s" % (device.alias,filetype), "w") as fh:
                                fh.write(parsed_output_type)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_totals)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals_mind_map.html" % (device.alias,device.alias))

                # Show interfaces
                if hasattr(self, 'parsed_show_int'):
                    sh_int_template = env.get_template('show_interfaces.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces/%s_show_int.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_int, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces/%s_show_int.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_int, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_int_template.render(to_parse_interfaces=self.parsed_show_int,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces/%s_show_int.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)  

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces/%s_show_int.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces/%s_show_int.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces/%s_show_int_mind_map.html" % (device.alias,device.alias))

                # Show interfaces status
                if hasattr(self, 'parsed_show_int_status'):
                    sh_int_status_template = env.get_template('show_int_status.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Status/%s_show_int_status.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_int_status, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Status/%s_show_int_status.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_int_status, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_int_status_template.render(to_parse_interfaces=self.parsed_show_int_status['interfaces'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Status/%s_show_int_status.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)  

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Status/%s_show_int_status.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Status/%s_show_int_status.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Status/%s_show_int_status_mind_map.html" % (device.alias,device.alias))

                # Show interfaces trunk
                if hasattr(self, 'parsed_show_interfaces_trunk'):
                    sh_interfaces_trunk_template = env.get_template('show_interfaces_trunk.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Trunk/%s_show_interfaces_trunk.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_interfaces_trunk, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Trunk/%s_show_interfaces_trunk.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_interfaces_trunk, yml, allow_unicode=True)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_interfaces_trunk_template.render(to_parse_interfaces_trunk=self.parsed_show_interfaces_trunk['interface'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Trunk/%s_show_interfaces_trunk.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Trunk/%s_show_interfaces_trunk.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Trunk/%s_show_interfaces_trunk.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Trunk/%s_show_interfaces_trunk_mind_map.html" % (device.alias,device.alias))

                # Show Inventory
                if hasattr(self, 'parsed_show_inventory'):
                    # 4500
                    sh_inventory_4500_template = env.get_template('show_inventory_4500.j2')

                    # 3850
                    sh_inventory_3850_template = env.get_template('show_inventory_3850.j2')

                    9300
                    sh_inventory_9300_template = env.get_template('show_inventory_9300.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        # 4500
                        if device.platform == "cat4500":
                            parsed_output_type = sh_inventory_4500_template.render(to_parse_inventory=self.parsed_show_inventory['main'],filetype_loop_jinja2=filetype)

                            with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.%s" % (device.alias,filetype), "w") as fh:
                                fh.write(parsed_output_type)

                            if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md" % device.alias):
                                os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                        # 3850
                        elif device.platform == "cat3850":
                            parsed_output_type = sh_inventory_3850_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],filetype_loop_jinja2=filetype)

                            with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.%s" % (device.alias,filetype), "w") as fh:
                                fh.write(parsed_output_type)

                            if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md" % device.alias):
                                os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                        # 9300
                        elif device.platform == "cat9300":
                            parsed_output_type = sh_inventory_9300_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],filetype_loop_jinja2=filetype)
  
                            with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.%s" % (device.alias,filetype), "w") as fh:
                                fh.write(parsed_output_type)

                            if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md" % device.alias):
                                os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                # Show ip arp
                if hasattr(self, 'parsed_show_ip_arp'):
                    sh_ip_arp_template = env.get_template('show_ip_arp.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP/%s_show_ip_arp.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ip_arp, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP/%s_show_ip_arp.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ip_arp, yml, allow_unicode=True)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_ip_arp_template.render(to_parse_ip_arp=self.parsed_show_ip_arp['interfaces'],filetype_loop_jinja2=filetype)
                      
                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP/%s_show_ip_arp.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP/%s_show_ip_arp.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP/%s_show_ip_arp.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP/%s_show_ip_arp_mind_map.html" % (device.alias,device.alias))

                # Show ip interface brief
                if hasattr(self, 'parsed_show_ip_int_brief'):
                    sh_ip_int_brief_template = env.get_template('show_ip_int_brief.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Interface_Brief/%s_show_ip_int_brief.json" % device.alias, "w") as fid:
                        json.dump(self.parsed_show_ip_int_brief, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Interface_Brief/%s_show_ip_int_brief.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.parsed_show_ip_int_brief, yml, allow_unicode=True)                 
        
                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_int_brief_template.render(to_parse_interfaces=self.parsed_show_ip_int_brief['interface'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Interface_Brief/%s_show_ip_int_brief.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Interface_Brief/%s_show_ip_int_brief.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Interface_Brief/%s_show_ip_int_brief.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Interface_Brief/%s_show_ip_int_brief_mind_map.html" % (device.alias,device.alias))

                # Show IP OSPF
                if hasattr(self, 'parsed_show_ip_ospf'):
                    sh_ip_ospf_template = env.get_template('show_ip_ospf.j2')
                    
                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF/%s_show_ip_ospf.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ip_ospf, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF/%s_show_ip_ospf.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ip_ospf, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_template.render(to_parse_ip_ospf=self.parsed_show_ip_ospf['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF/%s_show_ip_ospf.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF/%s_show_ip_ospf.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF/%s_show_ip_ospf.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF/%s_show_ip_ospf_mind_map.html" % (device.alias,device.alias))

                # Show IP OSPF Database
                if hasattr(self, 'parsed_show_ip_ospf_database'):
                    sh_ip_ospf_database_template = env.get_template('show_ip_ospf_database.j2')
                    
                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Database/%s_show_ip_ospf_database.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ip_ospf_database, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Database/%s_show_ip_ospf_database.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ip_ospf_database, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_database_template.render(to_parse_ip_ospf_database=self.parsed_show_ip_ospf_database['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Database/%s_show_ip_ospf_database.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Database/%s_show_ip_ospf_database.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Database/%s_show_ip_ospf_database.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Database/%s_show_ip_ospf_database_mind_map.html" % (device.alias,device.alias))

                # Show IP OSPF Interface
                if hasattr(self, 'parsed_show_ip_ospf_interface'):
                    sh_ip_ospf_interface_template = env.get_template('show_ip_ospf_interface.j2')
                    
                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ip_ospf_interface, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ip_ospf_interface, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_interface_template.render(to_parse_ip_ospf_interface=self.parsed_show_ip_ospf_interface['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface_mind_map.html" % (device.alias,device.alias))

                # Show IP OSPF Neighbor
                if hasattr(self, 'parsed_show_ip_ospf_neighbor'):
                    sh_ip_ospf_neighbor_template = env.get_template('show_ip_ospf_neighbor.j2')
                    
                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ip_ospf_neighbor, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ip_ospf_neighbor, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_neighbor_template.render(to_parse_ip_ospf_neighbor=self.parsed_show_ip_ospf_neighbor['interfaces'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor_mind_map.html" % (device.alias,device.alias))


                # Show IP OSPF Neighbor Detail
                if hasattr(self, 'parsed_show_ip_ospf_neighbor_detail'):
                    sh_ip_ospf_neighbor_detail_template = env.get_template('show_ip_ospf_neighbor_detail.j2')
                    
                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ip_ospf_neighbor_detail, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ip_ospf_neighbor_detail, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_neighbor_detail_template.render(to_parse_ip_ospf_neighbor_detail=self.parsed_show_ip_ospf_neighbor_detail['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail_mind_map.html" % (device.alias,device.alias))

                # Show IP Route
                if hasattr(self, 'parsed_show_ip_route'):
                    sh_ip_route_template = env.get_template('show_ip_route.j2')
                    sh_ip_route_netjson_json_template = env.get_template('show_ip_route_netjson_json.j2')
                    sh_ip_route_netjson_html_template = env.get_template('show_ip_route_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ip_route, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ip_route, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_route_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ip_route_netjson_json_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_route_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                # Show ISSU State Details
                if hasattr(self, 'parsed_show_issu_state'):
                    sh_issu_state_template = env.get_template('show_issu_state.j2')
                    
                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_issu_state, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_issu_state, yml, allow_unicode=True)                    
                    
                    for filetype in filetype_loop:
                        parsed_output_type = sh_issu_state_template.render(to_parse_issu_state=self.parsed_show_issu_state['slot'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type) 

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state_mind_map.html" % (device.alias,device.alias))

                # Show mac address-table
                if hasattr(self, 'parsed_show_mac_address_table'):
                    sh_mac_address_table_template = env.get_template('show_mac_address_table.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_MAC_Address_Table/%s_show_mac_address_table.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_mac_address_table, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_MAC_Address_Table/%s_show_mac_address_table.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_mac_address_table, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_mac_address_table_template.render(to_parse_mac_address_table=self.parsed_show_mac_address_table['mac_table'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_MAC_Address_Table/%s_show_mac_address_table.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_MAC_Address_Table/%s_show_mac_address_table.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_MAC_Address_Table/%s_show_mac_address_table.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_MAC_Address_Table/%s_show_mac_address_table_mind_map.html" % (device.alias,device.alias))

                # Show ntp associations
                if hasattr(self, 'parsed_show_ntp_associations'):
                    sh_ntp_associations_template = env.get_template('show_ntp_associations.j2')
                    
                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_NTP_Associations/%s_show_ntp_associations.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ntp_associations, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_NTP_Associations/%s_show_ntp_associations.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ntp_associations, yml, allow_unicode=True)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_ntp_associations_template.render(to_parse_ntp_associations=self.parsed_show_ntp_associations,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_NTP_Associations/%s_show_ntp_associations.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)                                                                     

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_NTP_Associations/%s_show_ntp_associations.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_NTP_Associations/%s_show_ntp_associations.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_NTP_Associations/%s_show_ntp_associations_mind_map.html" % (device.alias,device.alias))

                # Show power inline
                if hasattr(self, 'parsed_show_power_inline'):
                    sh_power_inline_template = env.get_template('show_power_inline.j2')
                    sh_power_inline_totals_template = env.get_template('show_power_inline_totals.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_power_inline, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_power_inline, yml, allow_unicode=True)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_power_inline_template.render(to_parse_power_inline=self.parsed_show_power_inline['interface'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)                                                                     

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline_mind_map.html" % (device.alias,device.alias))

                    total_avail_counter = 0
                    total_used_counter = 0

                    for interface,value in self.parsed_show_power_inline['interface'].items():          
                        total_avail_counter += value['max']
                        total_used_counter += value['power']

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_power_inline_totals_template.render(total_avail=total_avail_counter,total_used=total_used_counter,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline_totals.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)                                                                     

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline_totals.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline_totals.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline_totals_mind_map.html" % (device.alias,device.alias))

                # Show version
                if hasattr(self, 'parsed_show_version'):
                    sh_ver_template = env.get_template('show_version.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Version/%s_show_version.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_version, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Version/%s_show_version.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_version, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ver_template.render(to_parse_version=self.parsed_show_version['version'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Version/%s_show_version.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Version/%s_show_version.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Version/%s_show_version.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Version/%s_show_version_mind_map.html" % (device.alias,device.alias))

                # Show vlan
                if hasattr(self, 'parsed_show_vlan'):
                    sh_vlan_template = env.get_template('show_vlan.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_VLAN/%s_show_vlan.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_vlan, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_VLAN/%s_show_vlan.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_vlan, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_vlan_template.render(to_parse_vlan=self.parsed_show_vlan['vlans'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_VLAN/%s_show_vlan.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_VLAN/%s_show_vlan.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_VLAN/%s_show_vlan.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_VLAN/%s_show_vlan_mind_map.html" % (device.alias,device.alias))

                # Show vrf
                if hasattr(self, 'parsed_show_vrf'):
                    sh_vrf_template = env.get_template('show_vrf.j2')
                    sh_ip_arp_vrf_template = env.get_template('show_ip_arp.j2')
                    sh_ip_route_template = env.get_template('show_ip_route.j2')
                    
                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_VRF/%s_show_vrf.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_vrf, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_VRF/%s_show_vrf.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_vrf, yml, allow_unicode=True)

                    for filetype in filetype_loop:      
                        parsed_output_type = sh_vrf_template.render(to_parse_vrf=self.parsed_show_vrf['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_VRF/%s_show_vrf.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_VRF/%s_show_vrf.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_VRF/%s_show_vrf.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_VRF/%s_show_vrf_mind_map.html" % (device.alias,device.alias))

                    # For Each VRF
                    if device.type == "router":
                        for vrf in self.parsed_show_vrf['vrf']:
                      
                            # Show IP ARP VRF <VRF> 
                            with steps.start('Parsing ip arp vrf',continue_=True) as step:
                                try:
                                    self.parsed_show_ip_arp_vrf = device.parse("show ip arp vrf %s" % vrf)
                                except Exception as e:
                                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

                            with steps.start('Store data',continue_=True) as step:

                                with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                  json.dump(self.parsed_show_ip_arp_vrf, fid, indent=4, sort_keys=True)

                                with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                  yaml.dump(self.parsed_show_ip_arp_vrf, yml, allow_unicode=True)

                                for filetype in filetype_loop:
                                    parsed_output_type = sh_ip_arp_vrf_template.render(to_parse_ip_arp=self.parsed_show_ip_arp_vrf['interfaces'],filetype_loop_jinja2=filetype)

                                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                      fh.write(parsed_output_type)
        
                                if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.md" % (device.alias,vrf)):
                                    os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                            # Show IP ROUTE VRF <VRF> 
                            with steps.start('Parsing ip route vrf',continue_=True) as step:
                                try:
                                    self.parsed_show_ip_route_vrf = device.parse("show ip route vrf %s" % vrf)
                                except Exception as e:
                                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

                            with steps.start('Store data',continue_=True) as step:

                                with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                  json.dump(self.parsed_show_ip_route_vrf, fid, indent=4, sort_keys=True)

                                with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                  yaml.dump(self.parsed_show_ip_route_vrf, yml, allow_unicode=True)
                         
                                for filetype in filetype_loop:
                                    parsed_output_type = sh_ip_route_template.render(to_parse_ip_route=self.parsed_show_ip_route_vrf['vrf'],filetype_loop_jinja2=filetype)

                                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                      fh.write(parsed_output_type)

                                if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.md" % (device.alias,vrf)):
                                    os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED, justify="center")))