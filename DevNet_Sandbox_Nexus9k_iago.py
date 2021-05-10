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
from genie.utils.diff import Diff
from jinja2 import Environment, FileSystemLoader
from ascii_art import GREETING, LEARN, RUNNING, WRITING, PUSH_INTENT, FINISHED
from general_functionalities import ParseShowCommandFunction, ParseLearnFunction, ParseConfigFunction
from datetime import datetime
from contextlib import redirect_stdout

log = logging.getLogger(__name__)
template_dir = 'templates/cisco/nxos'
env = Environment(loader=FileSystemLoader(template_dir))
timestr = datetime.now().strftime("%Y%m%d_%H%M%S")

with open("data_models/DevNet_Sandbox_Nexus9k.yaml") as stream:
    data_model = yaml.safe_load(stream)

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
            # Genie learn('config').info for pre-change state 
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(LEARN, justify="center")))

            self.learned_config = ParseConfigFunction.parse_learn(steps, device, "config")
            original_learned_config = self.learned_config

            #----------------------------------------
            # Write Pre-Change File
            #----------------------------------------
            with steps.start('Store Original Golden Image',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING, justify="center")))
                
                original_config_filename = "%s_Original_Golden_Image_%s.json" % (timestr,device.alias)
                # Write Original Learned Config as JSON
                if hasattr(self, 'learned_config'):
                    with open("Iago/Golden_Image/%s" % original_config_filename, "w") as fid:
                        json.dump(self.learned_config, fid, indent=4, sort_keys=True)
                        fid.close()

            # ---------------------------------------
            # Create Intent from Template and Data Models
            # ---------------------------------------
            with steps.start('Generating Intent From Data Model and Template',continue_=True) as step:
                print(Panel.fit(Text.from_markup(RUNNING, justify="center")))
                intended_config_template = env.get_template('intended_config.j2')
                rendered_intended_config = intended_config_template.render(host_data_model=data_model)

                with open("Iago/Intended_Configs/%s_Intended_Config.txt" % timestr, "w") as fid:
                    fid.write(rendered_intended_config)
                    fid.close()
                
            # ---------------------------------------
            # Push Intent to Device 
            # ---------------------------------------         
            # with steps.start('Push Intent',continue_=True) as step:
                print(Panel.fit(Text.from_markup(PUSH_INTENT)))
                device.configure(rendered_intended_config)

            # ---------------------------------------
            # Re-capture state
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(LEARN, justify="center")))

            self.learned_config = ParseConfigFunction.parse_learn(steps, device, "config")
            new_learned_config = self.learned_config

            # ---------------------------------------
            # Write post-change state
            # ---------------------------------------
            with steps.start('Store New Golden Image',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING, justify="center")))
                
                new_config_filename = "%s_Golden_Image_%s.json" % (timestr,device.alias)

                # Write Original Learned Config as JSON
                if hasattr(self, 'learned_config'):
                    with open("Iago/Golden_Image/%s" % new_config_filename, "w") as fid:
                        json.dump(self.learned_config, fid, indent=4, sort_keys=True)
                        fid.close()

            # ---------------------------------------
            # Show the differential 
            # ---------------------------------------
            with steps.start('Show Differential',continue_=True) as step:
                print(Panel.fit(Text.from_markup(DIFF)))

                config_diff = Diff(original_learned_config, new_learned_config)
                config_diff.findDiff()
            
                if config_diff in locals():
                    print(Panel.fit(config_diff))
                
                    with open('Iago/Changes/%s_Changes.txt' % timestr, 'w') as f:
                        with redirect_stdout(f):
                            print(config_diff)
                            f.close()
                else:
                    print(Panel.fit("You have achieved [bright_blue]idempotency[/bright_blue] between your [bright_green]INTENT[/bright_green] and [bright_red]RUNNING[/bright_red] configurations"))
                    with open('Iago/Changes/%s_Changes.txt' % timestr, 'w') as f:
                        f.write("IDEMPOTENT - NO CHANGES")
                        f.close()

        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED, justify="center")))    