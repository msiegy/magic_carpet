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
from ascii_art import GREETING, LEARN, RUNNING, WRITING, FINISHED
from general_functionalities import ParseShowCommandFunction, ParseLearnFunction
from tinydb import TinyDB, Query

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
# Create Database
# ----------------

db = TinyDB('Cave_of_Wonders/Cisco/DevNet_Sandbox/Jafar/Nexus9K_Jafar_DB.json')
db.purge()

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

            # ----------------
            # Create a table in the database
            # ----------------
            table = db.table(device.alias)

            # ---------------------------------------
            # Genie learn().info for various functions
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(LEARN, justify="center")))

            # ACLs
            self.learned_acl = ParseLearnFunction.parse_learn(steps, device, "acl")

            # ARP
            self.learned_arp = ParseLearnFunction.parse_learn(steps, device, "arp")

            # BGP
            self.learned_bgp = ParseLearnFunction.parse_learn(steps, device, "bgp")

            # Interface
            self.learned_interface = ParseLearnFunction.parse_learn(steps, device, "interface")

            # OSPF
            self.learned_ospf = ParseLearnFunction.parse_learn(steps, device, "ospf")

            # Routing
            self.learned_routing = ParseLearnFunction.parse_learn(steps, device, "routing")

            # VLAN
            self.learned_vlan = ParseLearnFunction.parse_learn(steps, device, "vlan")

            # ---------------------------------------
            # Execute parser for various show commands
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(RUNNING, justify="center")))

            # Show Access-Lists
            self.parsed_show_access_lists = ParseShowCommandFunction.parse_show_command(steps, device, "show access-lists")

            # show bgp process vrf all
            self.parsed_show_bgp_process_vrf_all = ParseShowCommandFunction.parse_show_command(steps, device, "show bgp process vrf all")

            # Show BGP Sessions
            self.parsed_show_bgp_sessions = ParseShowCommandFunction.parse_show_command(steps, device, "show bgp sessions")

            # Show Interfaces Status
            self.parsed_show_int_status = ParseShowCommandFunction.parse_show_command(steps, device, "show interface status")

            # Show Inventory
            self.parsed_show_inventory = ParseShowCommandFunction.parse_show_command(steps, device, "show inventory")

            # Show IP Interface Brief
            self.parsed_show_ip_int_brief = ParseShowCommandFunction.parse_show_command(steps, device, "show ip interface brief")
            
            # Show IP OSPF
            self.parsed_show_ip_ospf = ParseShowCommandFunction.parse_show_command(steps, device, "show ip ospf")

            # Show IP Route
            self.parsed_show_ip_route = ParseShowCommandFunction.parse_show_command(steps, device, "show ip route")

            # Show MAC Address-Table
            self.parsed_show_mac_address_table = ParseShowCommandFunction.parse_show_command(steps, device, "show mac address-table")

            # Show Portchannel Summary
            self.parsed_show_port_channel_summary = ParseShowCommandFunction.parse_show_command(steps, device, "show port-channel summary")

            # Show Version
            self.parsed_show_version = ParseShowCommandFunction.parse_show_command(steps, device, "show version")

            # Show VLAN
            self.parsed_show_vlan = ParseShowCommandFunction.parse_show_command(steps, device, "show vlan")

            # Show VRF
            self.parsed_show_vrf = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf")

            # show VRF all detail
            self.parsed_show_vrf_all_detail = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf all detail")

            # show vrf all interface
            self.parsed_show_vrf_all_interface = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf all interface")

            # ---------------------------------------
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed Data
            # ---------------------------------------         

            with steps.start('Store data',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING, justify="center")))
                
                ###############################
                # Genie learn().info section
                ###############################

                # Learned ACL
                if hasattr(self, 'learned_acl'):
                    learned_acl_template = env.get_template('learned_acl.j2')
                    learned_acl_netjson_json_template = env.get_template('learned_acl_netjson_json.j2')
                    learned_acl_netjson_html_template = env.get_template('learned_acl_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.json" % device.alias, "w") as fid:
                        json.dump(self.learned_acl, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.learned_acl, yml, allow_unicode=True)                

                    for filetype in filetype_loop:
                        parsed_output_type = learned_acl_template.render(to_parse_access_list=self.learned_acl['acls'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_acl_netjson_json_template.render(to_parse_access_list=self.learned_acl['acls'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_acl_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store ACLs in Device Table in Database
                    # ----------------

                    table.insert(self.learned_acl)

                # Learned ARP
                if hasattr(self, 'learned_arp'):
                    learned_arp_template = env.get_template('learned_arp.j2')
                    learned_arp_statistics_template = env.get_template('learned_arp_statistics.j2')
                    learned_arp_netjson_json_template = env.get_template('learned_arp_netjson_json.j2')
                    learned_arp_netjson_html_template = env.get_template('learned_arp_netjson_html.j2')
                    learned_arp_statistics_netjson_json_template = env.get_template('learned_arp_statistics_netjson_json.j2')
                    learned_arp_statistics_netjson_html_template = env.get_template('learned_arp_statistics_netjson_html.j2')


                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp.json" % device.alias, "w") as fid:
                        json.dump(self.learned_arp, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.learned_arp, yml, allow_unicode=True)   

                    for filetype in filetype_loop:
                        parsed_output_type = learned_arp_template.render(to_parse_arp=self.learned_arp['interfaces'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 

                    for filetype in filetype_loop:
                        parsed_output_type = learned_arp_statistics_template.render(to_parse_arp=self.learned_arp['statistics'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_statistics.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_statistics.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_statistics_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_arp_netjson_json_template.render(to_parse_arp=self.learned_arp['interfaces'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_arp_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    parsed_output_netjson_json = learned_arp_statistics_netjson_json_template.render(to_parse_arp=self.learned_arp['statistics'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_arp_statistics_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_statistics_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_statistics_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store ARP in Device Table in Database
                    # ----------------

                    table.insert(self.learned_arp)

                # Learned BGP
                if hasattr(self, 'learned_bgp'):
                    learned_bgp_template = env.get_template('learned_bgp.j2')
                    learned_bgp_netjson_json_template = env.get_template('learned_bgp_netjson_json.j2')
                    learned_bgp_netjson_html_template = env.get_template('learned_bgp_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp.json" % device.alias, "w") as fid:
                        json.dump(self.learned_bgp, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.learned_bgp, yml, allow_unicode=True)   

                    for filetype in filetype_loop:
                        parsed_output_type = learned_bgp_template.render(to_parse_bgp=self.learned_bgp['instance'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_bgp_netjson_json_template.render(to_parse_bgp=self.learned_bgp['instance'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_bgp_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store BGP in Device Table in Database
                    # ----------------

                    table.insert(self.learned_bgp)

                # Learned Interface
                if hasattr(self, 'learned_interface'):
                    learned_interface_template = env.get_template('learned_interface.j2')
                    learned_interface_netjson_json_template = env.get_template('learned_interface_netjson_json.j2')
                    learned_interface_netjson_html_template = env.get_template('learned_interface_netjson_html.j2')
                    learned_interface_enable_netjson_json_template = env.get_template('learned_interface_enabled_netjson_json.j2')
                    learned_interface_enable_netjson_html_template = env.get_template('learned_interface_enabled_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface.json" % device.alias, "w") as fid:
                        json.dump(self.learned_interface, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.learned_interface, yml, allow_unicode=True)   

                    for filetype in filetype_loop:
                        parsed_output_type = learned_interface_template.render(to_parse_interface=self.learned_interface,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_interface_netjson_json_template.render(to_parse_interface=self.learned_interface,device_alias = device.alias)
                    parsed_output_netjson_html = learned_interface_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    parsed_output_netjson_json = learned_interface_enable_netjson_json_template.render(to_parse_interface=self.learned_interface,device_alias = device.alias)
                    parsed_output_netjson_html = learned_interface_enable_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface_enabled_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface_enabled_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)                        

                    # ----------------
                    # Store Interface in Device Table in Database
                    # ----------------

                    table.insert(self.learned_interface)

                # Learned OSPF
                if hasattr(self, 'learned_ospf'):
                    learned_ospf_template = env.get_template('learned_ospf.j2')
                    learned_ospf_netjson_json_template = env.get_template('learned_ospf_netjson_json.j2')
                    learned_ospf_netjson_html_template = env.get_template('learned_ospf_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_OSPF/%s_learned_ospf.json" % device.alias, "w") as fid:
                        json.dump(self.learned_ospf, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_OSPF/%s_learned_ospf.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.learned_ospf, yml, allow_unicode=True)   

                    # ----------------
                    # Store OSPF in Device Table in Database
                    # ----------------

                    table.insert(self.learned_ospf)

                # Learned Routing
                if self.learned_routing is not None:
                    learned_routing_template = env.get_template('learned_routing.j2')
                    learned_routing_netjson_json_template = env.get_template('learned_routing_netjson_json.j2')
                    learned_routing_netjson_html_template = env.get_template('learned_routing_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing.json" % device.alias, "w") as fid:
                        json.dump(self.learned_routing, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.learned_routing, yml, allow_unicode=True)                

                    for filetype in filetype_loop:
                        parsed_output_type = learned_routing_template.render(to_parse_routing=self.learned_routing['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_routing_netjson_json_template.render(to_parse_routing=self.learned_routing['vrf'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_routing_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store Routing in Device Table in Database
                    # ----------------

                    table.insert(self.learned_routing)

                # Learned VLAN
                if self.learned_vlan is not None:
                    learned_vlan_template = env.get_template('learned_vlan.j2')
                    learned_vlan_netjson_json_template = env.get_template('learned_vlan_netjson_json.j2')
                    learned_vlan_netjson_html_template = env.get_template('learned_vlan_netjson_html.j2')

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan.json" % device.alias, "w") as fid:
                        json.dump(self.learned_vlan, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.learned_vlan, yml, allow_unicode=True)                

                    for filetype in filetype_loop:
                        parsed_output_type = learned_vlan_template.render(to_parse_vlan=self.learned_vlan['vlans'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_vlan_netjson_json_template.render(to_parse_vlan=self.learned_vlan['vlans'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_vlan_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VLAN in Device Table in Database
                    # ----------------

                    table.insert(self.learned_vlan)

                ###############################
                # Genie Show Command Section
                ###############################

                # Show access-lists
                if hasattr(self, 'parsed_show_access_lists'):
                    sh_access_lists_template = env.get_template('show_access_lists.j2')                  
                    sh_access_lists_netjson_json_template = env.get_template('show_access_lists_netjson_json.j2')
                    sh_access_lists_netjson_html_template = env.get_template('show_access_lists_netjson_html.j2')

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

                    parsed_output_netjson_json = sh_access_lists_netjson_json_template.render(to_parse_access_list=self.parsed_show_access_lists,device_alias = device.alias)
                    parsed_output_netjson_html = sh_access_lists_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store ACLs in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_access_lists)

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

                    # ----------------
                    # Store BGP Process VRF All in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_bgp_process_vrf_all)

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

                    parsed_output_netjson_json = sh_bgp_sessions_netjson_json_template.render(to_parse_bgp=self.parsed_show_bgp_sessions,device_alias = device.alias)
                    parsed_output_netjson_html = sh_bgp_sessions_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store BGP Sessions in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_bgp_sessions)

                # Show interface status
                if hasattr(self, 'parsed_show_int_status'):
                    sh_int_status_template = env.get_template('show_int_status.j2')
                    sh_int_status_netjson_json_template = env.get_template('show_int_status_netjson_json.j2')
                    sh_int_status_netjson_html_template = env.get_template('show_int_status_netjson_html.j2')
                    sh_int_status_connected_netjson_json_template = env.get_template('show_int_status_connected_netjson_json.j2')
                    sh_int_status_connected_netjson_html_template = env.get_template('show_int_status_connected_netjson_html.j2')

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

                    parsed_output_netjson_json = sh_int_status_netjson_json_template.render(to_parse_interfaces=self.parsed_show_int_status['interfaces'],device_alias = device.alias)
                    parsed_output_netjson_html = sh_int_status_netjson_html_template.render(device_alias = device.alias)
                    parsed_output_connected_netjson_json = sh_int_status_connected_netjson_json_template.render(to_parse_interfaces=self.parsed_show_int_status['interfaces'],device_alias = device.alias)
                    parsed_output_connected_netjson_html = sh_int_status_connected_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status_connected_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_connected_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status_connected_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_connected_netjson_html)

                # Show Inventory
                if hasattr(self, 'parsed_show_inventory'):
                    # Nexus 
                    sh_inventory_nexus_template = env.get_template('show_inventory_nexus.j2')
                    sh_inventory_netjson_json_template = env.get_template('show_inventory_netjson_json.j2')
                    sh_inventory_netjson_html_template = env.get_template('show_inventory_netjson_html.j2')

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

                    parsed_output_netjson_json = sh_inventory_netjson_json_template.render(to_parse_inventory_name=self.parsed_show_inventory['name'],device_alias = device.alias)
                    parsed_output_netjson_html = sh_inventory_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store Inventory in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_inventory)

                # Show ip interface brief
                if hasattr(self, 'parsed_show_ip_int_brief'):
                    sh_ip_int_brief_template = env.get_template('show_ip_int_brief.j2')
                    sh_ip_int_brief_netjson_json_template = env.get_template('show_ip_int_brief_netjson_json.j2')
                    sh_ip_int_brief_netjson_html_template = env.get_template('show_ip_int_brief_netjson_html.j2')

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

                    parsed_output_netjson_json = sh_ip_int_brief_netjson_json_template.render(to_parse_interfaces=self.parsed_show_ip_int_brief['interface'],device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_int_brief_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store IP Int Brief in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_ip_int_brief)

                # Show IP OSPF
                if hasattr(self, 'parsed_show_ip_ospf'):
                    sh_ip_ospf_template = env.get_template('show_ip_ospf.j2')
                    sh_ip_ospf_netjson_json_template = env.get_template('show_ip_ospf_netjson_json.j2')
                    sh_ip_ospf_netjson_html_template = env.get_template('show_ip_ospf_netjson_html.j2')

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

                    parsed_output_netjson_json = sh_ip_ospf_netjson_json_template.render(to_parse_ip_route=self.parsed_show_ip_ospf['vrf'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_ospf_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store IP OSPF in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_ip_ospf)

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

                    # ----------------
                    # Store IP Route Brief in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_ip_route)

                # Show mac address-table
                if hasattr(self, 'parsed_show_mac_address_table'):
                    sh_mac_address_table_template = env.get_template('show_mac_address_table.j2')
                    sh_mac_address_netjson_json_template = env.get_template('show_mac_address_table_netjson_json.j2')
                    sh_mac_address_netjson_html_template = env.get_template('show_mac_address_table_netjson_html.j2')

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

                    parsed_output_netjson_json = sh_mac_address_netjson_json_template.render(to_parse_mac_address_table=self.parsed_show_mac_address_table['mac_table'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_mac_address_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store MAC Table in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_mac_address_table)

                # Show port-channel summary
                if hasattr(self, 'parsed_show_port_channel_summary'):
                    sh_portchannel_summary_template = env.get_template('show_portchannel_summary.j2')
                    sh_portchannel_summary_netjson_json_template = env.get_template('show_portchannel_summary_netjson_json.j2')
                    sh_portchannel_summary_netjson_html_template = env.get_template('show_portchannel_summary_netjson_html.j2')

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

                    parsed_output_netjson_json = sh_portchannel_summary_netjson_json_template.render(to_parse_etherchannel_summary=self.parsed_show_port_channel_summary['interfaces'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_portchannel_summary_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store Port-Channel in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_port_channel_summary)

                # Show version
                if hasattr(self, 'parsed_show_version'):
                    sh_ver_template = env.get_template('show_version.j2')
                    sh_ver_netjson_json_template = env.get_template('show_version_netjson_json.j2')
                    sh_ver_netjson_html_template = env.get_template('show_version_netjson_html.j2')

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

                    parsed_output_netjson_json = sh_ver_netjson_json_template.render(to_parse_version=self.parsed_show_version['platform'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_ver_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store Version in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_version)

                # Show vrf
                if hasattr(self, 'parsed_show_vrf'):
                    sh_vrf_template = env.get_template('show_vrf.j2')
                    sh_vrf_netjson_json_template = env.get_template('show_vrf_netjson_json.j2')
                    sh_vrf_netjson_html_template = env.get_template('show_vrf_netjson_html.j2') 
                    sh_ip_arp_vrf_template = env.get_template('show_ip_arp_vrf.j2')
                    sh_ip_arp_vrf_netjson_json_template = env.get_template('show_ip_arp_vrf_netjson_json.j2')
                    sh_ip_arp_vrf_netjson_html_template = env.get_template('show_ip_arp_vrf_netjson_html.j2')
                    sh_ip_arp_vrf_stats_template = env.get_template('show_ip_arp_vrf_statistics.j2')
                    sh_ip_route_vrf_netjson_json_template = env.get_template('show_ip_route_vrf_netjson_json.j2')
                    sh_ip_route_vrf_netjson_html_template = env.get_template('show_ip_route_vrf_netjson_html.j2')                    
                    
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

                    parsed_output_netjson_json = sh_vrf_netjson_json_template.render(to_parse_vrf=self.parsed_show_vrf['vrfs'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vrf_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VRF in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_vrf)

                # Show vrf all detail
                if hasattr(self, 'parsed_show_vrf_all_detail'):
                    sh_vrf_all_detail_template = env.get_template('show_vrf_all_detail.j2')
                    sh_vrf_all_detail_netjson_json_template = env.get_template('show_vrf_all_detail_netjson_json.j2')
                    sh_vrf_all_detail_netjson_html_template = env.get_template('show_vrf_all_detail_netjson_html.j2') 

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

                    parsed_output_netjson_json = sh_vrf_all_detail_netjson_json_template.render(to_parse_vrf=self.parsed_show_vrf_all_detail,filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vrf_all_detail_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VRF Detail in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_vrf_all_detail)

                # Show vrf all interface
                if hasattr(self, 'parsed_show_vrf_all_interface'):
                    sh_vrf_all_interface_template = env.get_template('show_vrf_all_interface.j2')
                    sh_vrf_all_interface_netjson_json_template = env.get_template('show_vrf_all_interface_netjson_json.j2')
                    sh_vrf_all_interface_netjson_html_template = env.get_template('show_vrf_all_interface_netjson_html.j2') 

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

                    parsed_output_netjson_json = sh_vrf_all_interface_netjson_json_template.render(to_parse_vrf=self.parsed_show_vrf_all_interface,filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vrf_all_interface_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VRF Interface in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_vrf_all_interface)

                # Show vlan
                if hasattr(self, 'parsed_show_vlan'):
                    sh_vlan_template = env.get_template('show_vlan.j2')
                    sh_vlan_netjson_json_template = env.get_template('show_vlan_netjson_json.j2')
                    sh_vlan_netjson_html_template = env.get_template('show_vlan_netjson_html.j2')  

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

                    parsed_output_netjson_json = sh_vlan_netjson_json_template.render(to_parse_vlan=self.parsed_show_vlan['vlans'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vlan_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VLAN Interface in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_vlan)

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

                            parsed_output_netjson_json = sh_ip_arp_vrf_netjson_json_template.render(to_parse_ip_arp=self.parsed_show_ip_arp_vrf['interfaces'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                            parsed_output_netjson_html = sh_ip_arp_vrf_netjson_html_template.render(device_alias = device.alias,vrf = vrf)

                            with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_netgraph.json" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_json)               

                            with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_netgraph.html" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_html)

                            # ----------------
                            # Store IP ARP VRF Interface in Device Table in Databse
                            # ----------------

                            table.insert(self.parsed_show_ip_arp_vrf)

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

                                parsed_output_netjson_json = sh_ip_route_vrf_netjson_json_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype,vrf = vrf,device_alias = device.alias)
                                parsed_output_netjson_html = sh_ip_route_vrf_netjson_html_template.render(device_alias = device.alias,vrf = vrf)

                                with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s_netgraph.json" % (device.alias,vrf), "w") as fh:
                                    fh.write(parsed_output_netjson_json)               

                                with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s_netgraph.html" % (device.alias,vrf), "w") as fh:
                                    fh.write(parsed_output_netjson_html)

                            # ----------------
                            # Store IP Route VRF Interface in Device Table in Databse
                            # ----------------

                            table.insert(self.parsed_show_ip_route_vrf)
        db.close()
        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED, justify="center")))
        with open('Cave_of_Wonders/Cisco/DevNet_Sandbox/Jafar/Nexus9K_Jafar_DB.json') as f:
            data = json.load(f)
 
        print("JSON file with 2 tables\n")
        print(json.dumps(data, indent = 4, sort_keys=True))                 