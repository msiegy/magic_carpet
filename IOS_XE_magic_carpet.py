# ----------------
# Copywrite
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
from os import path
from rich import print
from rich.panel import Panel
from rich.text import Text
from pyats import aetest
from pyats import topology
from pyats.log.utils import banner
from jinja2 import Environment, FileSystemLoader

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
        print(Panel.fit(Text.from_markup("Hang on tight - we are about to go on a [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/bold yellow][/blink] ride!\n\n[purple].-.\n[.-''-.,\n|  //`~\)\n(<|[/][blue]0[/][purple]|>[/][blue]0[/][purple])\n;\  _/ \\_ _\,\n__\|'._/_  \ '='-,\n/\ \    || )_///_\>>\n(  '._ T |\ | _/),-'\n'.   '._.-' /'/ |\n| '._   _.'`-.._/\n,\ / '-' |/\n[_/\-----j\n_.--.__[_.--'_\__\n/         `--'    '---._\n/ '---.  -'. .'  _.--   '.\n\_      '--.___ _;.-o     /\n'.__ ___/______.__8----'\nc-'----'[/]\n\n",justify="center")))
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
            # Execute parser for various show commands
            # ---------------------------------------
            print(Panel.fit(Text.from_markup("[blue]_.---.__\n.'        `-.\n/      .--.   |\n\/  / /    |_/\n`\/|/    _(_)\n___  /|_.--'    `.   .\n\  `--' .---.     \ /|\n)   `       \     //|\n| __    __   |   '/||\n|/  \  /  \      / ||\n||  |  |   \     \  |\n\|  |  |   /        |\n__\\@/  |@ | ___ \--'\n(     /' `--'  __)|\n__>   (  .  .--' & \n/   `--|_/--'     &  |\n|                 #. |\n|                 q# |\n\              ,ad#'\n`.________.ad####'\n`#####''''''\n`&#\n&# #&\n'#ba'\n'[/]\n\nThe [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/][/blink] is heading into the [bold cyan]Cave of Wonders[/bold cyan]\n\n[bold blue]Genie[/bold blue] Parsing Has Begun",justify="center")))

            # Show Access-Lists
            with steps.start('Parsing show access-lists',continue_=True) as step:
                try:
                    self.parsed_show_access_lists = device.parse("show access-lists")
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
                    self.parsed_show_cdp_neighbors = device.parse("show cdp neighbors detail")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Etherchannel Summary
            with steps.start('Parsing show etherchannel summary',continue_=True) as step:
                try:
                    self.parsed_show_etherchannel_summary = device.parse("show etherchannel summary")
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

            # Show IP OSF Neighbor Detail - Layer 3 Command only 
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

            # Show Version
            with steps.start('Parsing show version',continue_=True) as step:
                try:
                    self.parsed_show_version = device.parse("show version")
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
            # Create JSON, YAML, CSV, MD, HTML files from the Parsed Data
            # ---------------------------------------         
            
            with steps.start('Store data',continue_=True) as step:

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
                    
                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists_mind_map.html" % (device.alias,device.alias))

                # Show Authentication Sessions
                if hasattr(self, 'parsed_show_authentication_sessions'):
                    sh_authetication_sessions_template = env.get_template('show_authentication_sessions.j2')                  

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_authentication_sessions, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_authentication_sessions, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_authetication_sessions_template.render(to_parse_authentication_sessions=self.parsed_show_authentication_sessions['interfaces'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.html" % (device.alias,device.alias))

                # Show CDP Neighbors
                if hasattr(self, 'parsed_show_cdp_neighbors'):
                    sh_cdp_neighbors_template = env.get_template('show_cdp_neighbors.j2')
                    sh_cdp_neighbors_totals_template = env.get_template('show_cdp_neighbors_totals.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_cdp_neighbors, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_cdp_neighbors, yml, allow_unicode=True)

                    for filetype in filetype_loop:                    
                        parsed_output_type = sh_cdp_neighbors_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors['index'],filetype_loop_jinja2=filetype)
                        parsed_totals = sh_cdp_neighbors_totals_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                        if path.exists(os.path.join('Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/',device.alias,'_show_cdp_neighbors.md')):
                            os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_mind_map.html" % (device.alias,device.alias))

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_totals.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_totals)

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_totals.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_totals_mind_map.html" % (device.alias,device.alias))

                # Show etherchannel summary
                if hasattr(self, 'parsed_show_etherchannel_summary'):
                    sh_etherchannel_summary_template = env.get_template('show_etherchannel_summary.j2')
                    sh_etherchannel_summary_totals_template = env.get_template('show_etherchannel_summary_totals.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_etherchannel_summary, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_etherchannel_summary, yml, allow_unicode=True)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_etherchannel_summary_template.render(to_parse_etherchannel_summary=self.parsed_show_etherchannel_summary['interfaces'],filetype_loop_jinja2=filetype)
                        parsed_totals = sh_etherchannel_summary_totals_template.render(to_parse_etherchannel_summary=self.parsed_show_etherchannel_summary,filetype_loop_jinja2=filetype)
                      
                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_totals)

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_mind_map.html" % (device.alias,device.alias))

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.html" % (device.alias,device.alias))

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

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Status/%s_show_int_status.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Status/%s_show_int_status_mind_map.html" % (device.alias,device.alias))

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

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Trunk/%s_show_interfaces_trunk.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Interfaces_Trunk/%s_show_interfaces_trunk_mind_map.html" % (device.alias,device.alias))

                # Show Inventory
                if hasattr(self, 'parsed_show_inventory'):
                    # 4500
                    sh_inventory_4500_template = env.get_template('show_inventory_4500.j2')

                    # 3850
                    sh_inventory_3850_template = env.get_template('show_inventory_3850.j2')

                    # 9300
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

                            os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                        # 3850
                        elif device.platform == "cat3850":
                            parsed_output_type = sh_inventory_3850_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],filetype_loop_jinja2=filetype)

                            with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.%s" % (device.alias,filetype), "w") as fh:
                                fh.write(parsed_output_type)

                            os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                        # 9300
                        elif device.platform == "cat9k":
                            parsed_output_type = sh_inventory_9300_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],filetype_loop_jinja2=filetype)
  
                            with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.%s" % (device.alias,filetype), "w") as fh:
                                fh.write(parsed_output_type)

                            os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

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

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP/%s_show_ip_arp.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP/%s_show_ip_arp_mind_map.html" % (device.alias,device.alias))

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

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Interface_Brief/%s_show_ip_int_brief.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Interface_Brief/%s_show_ip_int_brief_mind_map.html" % (device.alias,device.alias))

                # Show IP OSPF Neighbor Detail
                if hasattr(self, 'parsed_show_ip_ospf_neighbor_detail'):
                    sh_ip_ospf_neighbor_detail_template = env.get_template('show_ip_ospf_neighbor_detail.j2')
                    
                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor_detail.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ip_ospf_neighbor_detail, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor_detail.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ip_ospf_neighbor_detail, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_neighbor_detail_template.render(to_parse_ip_ospf_neighbor_detail=self.parsed_show_ip_ospf_neighbor_detail['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor_detail.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor_detail.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor_detail_mind_map.html" % (device.alias,device.alias))

                # Show IP Route
                if hasattr(self, 'parsed_show_ip_route'):
                    sh_ip_route_template = env.get_template('show_ip_route.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_ip_route, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_ip_route, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_route_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)
                    
                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route_mind_map.html" % (device.alias,device.alias))

                # Show ISSU State Details
                if hasattr(self, 'parsed_show_cdp_neighbors'):
                    sh_issu_state_template = env.get_template('show_issu_state.j2')
                    
                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_issu_state, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_issu_state, yml, allow_unicode=True)                    
                    
                    for filetype in filetype_loop:
                        parsed_output_type = sh_issu_state_template.render(to_parse_issu_state=self.parsed_show_issu_state['slot'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type) 

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state_mind_map.html" % (device.alias,device.alias))

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

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_MAC_Address_Table/%s_show_mac_address_table.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_MAC_Address_Table/%s_show_mac_address_table_mind_map.html" % (device.alias,device.alias))

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

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_NTP_Associations/%s_show_ntp_associations.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_NTP_Associations/%s_show_ntp_associations_mind_map.html" % (device.alias,device.alias))

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

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_Version/%s_show_version.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Version/%s_show_version.html" % (device.alias,device.alias))

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

                    os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_VRF/%s_show_vrf.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_VRF/%s_show_vrf.html" % (device.alias,device.alias))

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
        
                                os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.html" % (device.alias,device.alias,device.alias,device.alias))

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

                                os.system("markmap Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.html" % (device.alias,device.alias,device.alias,device.alias))

        # For loop done - We're done here!
        # Copy all Wonders to runinfo so it is visible in the logviewer
        # Not working - but should work next week - This would allow to 
        # see all the Wonders in the brower too!
        # shutil.copytree('Wonders', os.path.join(self.parameters['runinfo_dir'], 'Wonders'))

        # Goodbye Banner
        print(Panel.fit(Text.from_markup("You've made it out of the [bold orange]Cave of Wonders[/bold orange] on your [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/][/blink]!\n[green]What treasures did you get?[/green]\n\n[bold yellow]_[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]_[/]\n([bold yellow][blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink][/])\n)`#####`(\n/         \ \n|  [bold green]NETWORK[/bold green]  |\n|  [bold green]D A T A[/bold green]  |\n\           /\n`=========`\n\n\n\nYour Network Data can be found in the [bold cyan]Cave of Wonders[/bold cyan]\n\nType cd [bold cyan]Cave_of_Wonders[/bold cyan]\n\nTo see the log of your [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/][/blink] ride \nType [bold red]pyats logs view[/bold red]\n\nWritten by John Capobianco March 2021",justify="center")))