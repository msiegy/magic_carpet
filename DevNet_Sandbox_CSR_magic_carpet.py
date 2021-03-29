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
            # Execute parser for various show commands
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(RUNNING, justify="center")))

            # Show Access-Lists
            with steps.start('Parsing show access-lists',continue_=True) as step:
                try:
                    self.parsed_show_access_lists = device.parse("show access-lists")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Etherchannel Summary
            with steps.start('Parsing show etherchannel summary',continue_=True) as step:
                try:
                    self.parsed_show_etherchannel_summary = device.parse("show etherchannel summary")
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

            # Show IP Route - Layer 3 Command Only
            if device.type == "router":
                with steps.start('Parsing show ip route',continue_=True) as step:
                    try:
                        self.parsed_show_ip_route = device.parse("show ip route")
                    except Exception as e:
                        step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # Show Version
            with steps.start('Parsing show version',continue_=True) as step:
                try:
                    self.parsed_show_version = device.parse("show version")
                except Exception as e:
                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

            # ---------------------------------------
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed Data
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
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists_mind_map.html" % (device.alias,device.alias))

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

                # Show Inventory
                if hasattr(self, 'parsed_show_inventory'):
                    # CSR100v
                    sh_inventory_csr100v_template = env.get_template('show_inventory_CSR100v.j2')

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.json" % device.alias, "w") as fid:
                      json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)

                    with open("Cave_of_Wonders/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.yaml" % device.alias, "w") as yml:
                      yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_inventory_csr100v_template.render(to_parse_inventory_slot=self.parsed_show_inventory['slot'],to_parse_inventory_main=self.parsed_show_inventory['main'],filetype_loop_jinja2=filetype)

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
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.md --output Cave_of_Wonders/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route_mind_map.html" % (device.alias,device.alias))

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

        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED, justify="center")))            