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
from genie.libs.conf.device.iosxe.device import Device
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

template_dir = 'templates/cisco/ios_xe'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# Create Database
# ----------------

db = TinyDB('Cave_of_Wonders/Cisco/DevNet_Sandbox/Jafar/CSR1000v_Jafar_DB.json')
db.truncate()

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

            # Dot1X
            self.learned_dot1x = ParseLearnFunction.parse_learn(steps, device, "dot1x")            

            # Interface
            self.learned_interface = ParseLearnFunction.parse_learn(steps, device, "interface")

            # Routing
            self.learned_routing = ParseLearnFunction.parse_learn(steps, device, "routing")

            # ---------------------------------------
            # Execute parser for various show commands
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(RUNNING, justify="center")))

            # Show Access-Lists
            self.parsed_show_access_lists = ParseShowCommandFunction.parse_show_command(steps, device, "show access-lists")

            # Show Etherchannel Summary
            self.parsed_show_etherchannel_summary = ParseShowCommandFunction.parse_show_command(steps, device, "show etherchannel summary")
            
            # Show Inventory
            self.parsed_show_inventory = ParseShowCommandFunction.parse_show_command(steps, device, "show inventory")

            # Show IP ARP - Layer 3 Command only
            self.parsed_show_ip_arp = ParseShowCommandFunction.parse_show_command(steps, device, "show ip arp")

            # Show IP Interface Brief
            self.parsed_show_ip_int_brief = ParseShowCommandFunction.parse_show_command(steps, device, "show ip interface brief")

            # Show IP Route - Layer 3 Command Only
            self.parsed_show_ip_route = ParseShowCommandFunction.parse_show_command(steps, device, "show ip route")

            # Show Version
            self.parsed_show_version = ParseShowCommandFunction.parse_show_command(steps, device, "show version")

            # ---------------------------------------
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed Data
            # ---------------------------------------         
            
            with steps.start('Store data',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING, justify="center")))
                
                ###############################
                # Genie learn().info section
                ###############################

                # Learned ACL
                if self.learned_acl is not None:
                    learned_acl_template = env.get_template('learned_acl.j2')
                    learned_acl_netjson_json_template = env.get_template('learned_acl_netjson_json.j2')
                    learned_acl_netjson_html_template = env.get_template('learned_acl_netjson_html.j2')
                    directory_names = "Learned_ACL"
                    file_names = "learned_acl" 

                    self.save_to_json_file(device, directory_names, file_names, self.learned_acl)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.yaml" % device.alias, "w") as yml:
                        yaml.dump(self.learned_acl, yml, allow_unicode=True)
                        yml.close()           

                    for filetype in filetype_loop:
                        parsed_output_type = learned_acl_template.render(to_parse_access_list=self.learned_acl['acls'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                            fh.close()
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_acl_netjson_json_template.render(to_parse_access_list=self.learned_acl['acls'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_acl_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()        

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store ACLs in Device Table in Database
                    # ----------------

                    table.insert(self.learned_acl)

                # Learned ARP
                if self.learned_arp is not None:
                    learned_arp_template = env.get_template('learned_arp.j2')
                    learned_arp_statistics_template = env.get_template('learned_arp_statistics.j2')
                    learned_arp_netjson_json_template = env.get_template('learned_arp_netjson_json.j2')
                    learned_arp_netjson_html_template = env.get_template('learned_arp_netjson_html.j2')
                    learned_arp_statistics_netjson_json_template = env.get_template('learned_arp_statistics_netjson_json.j2')
                    learned_arp_statistics_netjson_html_template = env.get_template('learned_arp_statistics_netjson_html.j2')

                    directory = "Learned_ARP"
                    filename = "learned_arp"

                    self.save_to_json_file(device, directory, filename, self.learned_arp)
                    self.save_to_yaml_file(device, directory, filename, self.learned_arp)

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

                    # interface netjson
                    parsed_output_netjson_json = learned_arp_netjson_json_template.render(to_parse_arp=self.learned_arp['interfaces'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_arp_netjson_html_template.render(device_alias = device.alias)
                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # interface statistics netjson
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

                # Learned Dot1X
                if self.learned_dot1x is not None:
                    learned_dot1x_template = env.get_template('learned_dot1x.j2')
                    learned_dot1x_netjson_json_template = env.get_template('learned_dot1x_netjson_json.j2')
                    learned_dot1x_netjson_html_template = env.get_template('learned_dot1x_netjson_html.j2')
                    learned_dot1x_sessions_template = env.get_template('learned_dot1x_sessions.j2')
                    learned_dot1x_sessions_netjson_json_template = env.get_template('learned_dot1x_sessions_netjson_json.j2')
                    learned_dot1x_sessions_netjson_html_template = env.get_template('learned_dot1x_sessions_netjson_html.j2')
                    directory = "Learned_Dot1X"
                    filename = "learned_dot1x"
                    
                    self.save_to_json_file(device, directory, filename, self.learned_dot1x)
                    self.save_to_yaml_file(device, directory, filename, self.learned_dot1x)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_dot1x_template.render(to_parse_dot1x=self.learned_dot1x,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                            fh.close()
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_dot1x_netjson_json_template.render(to_parse_dot1x=self.learned_dot1x,device_alias = device.alias)
                    parsed_output_netjson_html = learned_dot1x_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json) 
                        fh.close()              

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    for filetype in filetype_loop:
                        parsed_output_type = learned_dot1x_sessions_template.render(to_parse_dot1x=self.learned_dot1x,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x_sessions.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                            fh.close()
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x_sessions.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x_sessions.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x_sessions_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_dot1x_sessions_netjson_json_template.render(to_parse_dot1x=self.learned_dot1x,device_alias = device.alias)
                    parsed_output_netjson_html = learned_dot1x_sessions_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x_sessions_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               
                        fh.close()

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Dot1X/%s_learned_dot1x_sessions_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store dot1X in Device Table in Database
                    # ----------------

                    table.insert(self.learned_dot1x)

                # Learned Interface
                if self.learned_interface is not None:
                    learned_interface_template = env.get_template('learned_interface.j2')
                    learned_interface_netjson_json_template = env.get_template('learned_interface_netjson_json.j2')
                    learned_interface_netjson_html_template = env.get_template('learned_interface_netjson_html.j2')
                    learned_interface_enable_netjson_json_template = env.get_template('learned_interface_enabled_netjson_json.j2')
                    learned_interface_enable_netjson_html_template = env.get_template('learned_interface_enabled_netjson_html.j2')
                    learned_interface_directory = "Learned_Interface"
                    learned_interface_file_name = "learned_interface"

                    self.save_to_json_file(device, learned_interface_directory, learned_interface_file_name, self.learned_interface)
                    self.save_to_yaml_file(device, learned_interface_directory, learned_interface_file_name, self.learned_interface)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_interface_template.render(to_parse_interface=self.learned_interface,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)     

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface_mind_map.html" % (device.alias,device.alias))

                    # now lets deal with netgraph
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

                # Learned Routing
                if self.learned_routing is not None:
                    learned_routing_template = env.get_template('learned_routing.j2')
                    learned_routing_netjson_json_template = env.get_template('learned_routing_netjson_json.j2')
                    learned_routing_netjson_html_template = env.get_template('learned_routing_netjson_html.j2')

                    directory = "Learned_Routing"
                    filename = "learned_routing"

                    self.save_to_json_file(device, directory, filename, self.learned_routing)
                    self.save_to_yaml_file(device, directory, filename, self.learned_routing)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_routing_template.render(to_parse_routing=self.learned_routing['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                            fh.close()
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_routing_netjson_json_template.render(to_parse_routing=self.learned_routing['vrf'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_routing_netjson_html_template.render(device_alias = device.alias)

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()

                    with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store Routing in Device Table in Database
                    # ----------------

                    table.insert(self.learned_routing)

                ###############################
                # Genie Show Command Section
                ###############################

                # Show access-lists
                if self.parsed_show_access_lists is not None:
                    sh_access_lists_template = env.get_template('show_access_lists.j2')    
                    show_access_lists_directory = "Show_Access_Lists"
                    show_access_lists_filename = "show_access_lists"

                    self.save_to_json_file(device, show_access_lists_directory, show_access_lists_filename, self.parsed_show_access_lists)
                    self.save_to_yaml_file(device, show_access_lists_directory, show_access_lists_filename, self.parsed_show_access_lists)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_access_lists_template.render(to_parse_access_list=self.parsed_show_access_lists,filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                            fh.close()
                    
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store ACLs in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_access_lists)

                # Show etherchannel summary
                if self.parsed_show_etherchannel_summary is not None:
                    sh_etherchannel_summary_template = env.get_template('show_etherchannel_summary.j2')
                    sh_etherchannel_summary_totals_template = env.get_template('show_etherchannel_summary_totals.j2')

                    sh_etherchannel_summary_directory = "Show_Etherchannel_Summary"
                    sh_etherchannel_summary_filename = "show_etherchannel_summary"

                    self.save_to_json_file(device, sh_etherchannel_summary_directory, sh_etherchannel_summary_filename, self.parsed_show_etherchannel_summary)
                    self.save_to_yaml_file(device, sh_etherchannel_summary_directory, sh_etherchannel_summary_filename, self.parsed_show_etherchannel_summary)

                    for filetype in filetype_loop: 
                        # parsed_output_type is None just in case the "if parsed_output_type in locals()" loop below fails. 
                        # In which case, we will an error since we called the variable before variable assignment. 
                        # Almost like calling something that does not yet exist. 
                        parsed_output_type = None

                        if 'interfaces' in self.parsed_show_etherchannel_summary:                          
                            parsed_output_type = sh_etherchannel_summary_template.render(to_parse_etherchannel_summary=self.parsed_show_etherchannel_summary['interfaces'],filetype_loop_jinja2=filetype)
                        parsed_totals = sh_etherchannel_summary_totals_template.render(to_parse_etherchannel_summary=self.parsed_show_etherchannel_summary,filetype_loop_jinja2=filetype)
                      
                        if parsed_output_type in locals():                                                    
                            with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Etherchannel_Summary/%s_show_etherchannel_summary.%s" % (device.alias,filetype), "w") as fh:
                                fh.write(parsed_output_type)
                                fh.close()

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_totals)
                          fh.close()

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Etherchannel_Summary/%s_show_etherchannel_summary.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Etherchannel_Summary/%s_show_etherchannel_summary.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Etherchannel_Summary/%s_show_etherchannel_summary_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store EtherChannel in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_etherchannel_summary)

                # Show Inventory
                if self.parsed_show_inventory is not None:
                    # CSR100v
                    sh_inventory_csr100v_template = env.get_template('show_inventory_CSR100v.j2')
                    
                    directory = "Show_Inventory"
                    filename = "show_inventory" 

                    self.save_to_json_file(device, directory, filename, self.parsed_show_inventory)
                    self.save_to_yaml_file(device, directory, filename, self.parsed_show_inventory)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_inventory_csr100v_template.render(to_parse_inventory_slot=self.parsed_show_inventory['slot'],to_parse_inventory_main=self.parsed_show_inventory['main'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)
                            fh.close()

                        if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory.md" % device.alias):
                            os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store Inventory in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_inventory)

                # Show ip arp
                if self.parsed_show_ip_arp is not None:
                    sh_ip_arp_template = env.get_template('show_ip_arp.j2')
                    directory = "Show_IP_ARP"
                    filename = "show_ip_arp"

                    self.save_to_json_file(device, directory, filename, self.parsed_show_ip_arp)
                    self.save_to_yaml_file(device, directory, filename, self.parsed_show_ip_arp)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_ip_arp_template.render(to_parse_ip_arp=self.parsed_show_ip_arp['interfaces'],filetype_loop_jinja2=filetype)
                      
                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP/%s_show_ip_arp.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)
                          fh.close()

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP/%s_show_ip_arp.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP/%s_show_ip_arp.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_ARP/%s_show_ip_arp_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store IP ARP in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_arp)

                # Show ip interface brief
                if self.parsed_show_ip_int_brief is not None:
                    sh_ip_int_brief_template = env.get_template('show_ip_int_brief.j2')
                    directory = "Show_IP_Interface_Brief"
                    filename = "show_ip_int_brief"
                    
                    self.save_to_json_file(device, directory, filename, self.parsed_show_ip_int_brief)
                    self.save_to_yaml_file(device, directory, filename, self.parsed_show_ip_int_brief)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_int_brief_template.render(to_parse_interfaces=self.parsed_show_ip_int_brief['interface'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)
                            fh.close()

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store IP Int Brief in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_int_brief)

                # Show IP Route
                if self.parsed_show_ip_route is not None:
                    sh_ip_route_template = env.get_template('show_ip_route.j2')
                    directory = "Show_IP_Route"
                    filename = "show_ip_route"

                    self.save_to_json_file(device, directory, filename, self.parsed_show_ip_route)
                    self.save_to_yaml_file(device, directory, filename, self.parsed_show_ip_route)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_route_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)
                          fh.close()
                                        
                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store IP Route Brief in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_route)

                # Show version
                if self.parsed_show_version is not None:
                    sh_ver_template = env.get_template('show_version.j2')
                    directory = "Show_Version"
                    filename = "show_version"

                    self.save_to_json_file(device, directory, filename, self.parsed_show_version)
                    self.save_to_yaml_file(device, directory, filename, self.parsed_show_version)
                    
                    for filetype in filetype_loop:
                        parsed_output_type = sh_ver_template.render(to_parse_version=self.parsed_show_version['version'],filetype_loop_jinja2=filetype)

                        with open("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)
                            fh.close()

                    if os.path.exists("Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version.md" % device.alias):
                        os.system("markmap --no-open Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version.md --output Cave_of_Wonders/Cisco/DevNet_Sandbox/Show_Version/%s_show_version_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store Version in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_version)

        db.close()
        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED, justify="center")))

        with open('Cave_of_Wonders/Cisco/DevNet_Sandbox/Jafar/CSR1000v_Jafar_DB.json') as f:
            data = json.load(f)
            f.close()
 
        print("JSON file with 2 tables\n")
        print(json.dumps(data, indent = 4, sort_keys=True))     
    

    """
    Meant to dump data to json. For example, in the case of Access Lists, where we would do: 
    We now call save_to_json_file(device, "Learned_ACL", "learned_acl", self.learned_acl)
    would create a file inside "Cave_of_Wonders/Cisco/DevNet_Sandbox/Learned_ACL/[device.alias].json"
    """
    def save_to_json_file(self, device, directory, file_name, content):
        file_path = "Cave_of_Wonders/Cisco/DevNet_Sandbox/{}/{}_{}.json".format(directory, device.alias, file_name)
        with open(file_path, "w") as json_file:
            json.dump(content, json_file, indent=4, sort_keys=True)
            json_file.close()
    
    def save_to_yaml_file(self, device, directory, file_name, content):
        file_path = "Cave_of_Wonders/Cisco/DevNet_Sandbox/{}/{}_{}.yaml".format(directory, device.alias, file_name)
        with open(file_path, "w") as yml_file:
            yaml.dump(content, yml_file, allow_unicode=True)
            yml_file.close()
    
    def save_to_specified_file_type(self, device, directory, file_name, content, file_type):
        file_path = "Cave_of_Wonders/Cisco/DevNet_Sandbox/{}/{}_{}.{}".format(directory, device.alias, file_name, file_type)
        with open(file_path, "w") as opened_file:
            opened_file.write(content)
            opened_file.close()