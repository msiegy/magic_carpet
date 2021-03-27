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
from rich import print
from rich.panel import Panel
from rich.text import Text
from pyats import aetest
from pyats import topology
from pyats.log.utils import banner
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from jinja2 import Environment, FileSystemLoader
from ascii_art import GREETING, RUNNING


# ----------------
# Get logger for script
# ----------------

log = logging.getLogger(__name__)

# ----------------
# Filetypes
# ----------------

filetype_loop = ["csv", "md", "html"]

# ----------------
# Template Directory
# ----------------

template_dir = 'templates/cisco/ios_xe/dynamic'
output_dir = 'Cave_of_Wonders/Cisco/IOS_XE'
env = Environment(loader=FileSystemLoader(template_dir))


def generator(template_path):

    patterns = ["_totals", '_discord', '_3850', '_4500', '_9300']
    templates = os.listdir(template_path)
    cmds = {template: " ".join(template.split('.')[0].split('_'))
            for template in templates}
    for template in cmds:
        for pattern in patterns:
            if pattern in template:
                command = cmds[template].replace(pattern.replace("_", " "), "")
                break
            else:
                command = cmds[template]
        output = {'command': command,
                  'template': template}
        yield output


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
    def greeting(self, testbed, section, steps):
        print(Panel.fit(Text.from_markup(RUNNING, justify="center")))

    @aetest.test.loop(data=generator(template_dir))
    def parse(self, testbed, section, steps, data):
        """ Testcase Setup section """
        section.uid = data['template']
        switch_templates = ['show_interfaces_trunk.j2', 'show_int_status.j2',
                            'show_issu_state.j2', 'show_mac_address_table.j2']
        # ---------------------------------------
        # Loop over devices
        # ---------------------------------------
        for device in testbed:
            cmd = data['command']
            cmd_dir = data['template'].split('.')[0]
            template = data['template']

            if device.type == "router" and template in switch_templates :
                print("Entrei")
                continue

            try:
                parsed_data = device.parse(cmd)
                template = env.get_template(template)
        # ---------------------------------------
        # Create Folder if not exist
        # ---------------------------------------
                if( not os.path.exists(f"{output_dir}/{cmd_dir}") ):
                    pwd = os.getcwd()
                    path = f"{output_dir}/{cmd_dir}"
                    os.mkdir(os.path.join(pwd, path))
        # ---------------------------------------
        # Create JSON FILE
        # ---------------------------------------
                with open(f"{output_dir}/{cmd_dir}/{device.alias}_{cmd_dir}.json", "w+") as fh:
                    json.dump(parsed_data, fh, indent=4, sort_keys=True)
        # ---------------------------------------
        # Create YAML FILE
        # ---------------------------------------
                with open(f"{output_dir}/{cmd_dir}/{device.alias}_{cmd_dir}.yaml", "w+") as fh:
                    yaml.dump(parsed_data, fh, indent=4, allow_unicode=True)
        # ---------------------------------------
        # Create FILES by filetype
        # ---------------------------------------
                for filetype in filetype_loop:
                    parsed_output = template.render(data=parsed_data, filetype_loopjinja2=filetype)
                    with open(f"{output_dir}/{cmd_dir}/{device.alias}_{cmd_dir}.{filetype}", "w+") as fh:
                        fh.write(parsed_output)
        # ---------------------------------------
        # Create markmap
        # ---------------------------------------
                os.system(f"markmap {output_dir}/{cmd_dir}/{device.alias}_{cmd_dir}.md" \
                           " --output {output_dir}/{cmd_dir}/{device.alias}_{cmd_dir}_mind_map.html")

            except SchemaEmptyParserError as e:
                self.skipped("No data")

            except Exception as e:
                self.errored(
                            reason=f"Could not parse it correctly",
                            from_exception=e,)


class common_cleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect_all(self, testbed):
        for device in testbed:
            device.disconnect()

