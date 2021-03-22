# ----------------
# Copywrite
# ----------------
# Written by John Capobianco, March 2021
# Copyright (c) 2021 John Capobianco

# ----------------
# Python
# ----------------
import yaml
import json
import logging
from rich import print
from rich.panel import Panel
from rich.text import Text
from pyats import aetest


# ----------------
# Jinja2
# ----------------
from jinja2 import Environment, FileSystemLoader

template_dir = "templates/juniper"
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# Import pyATS and the pyATS Library
# ----------------

# Get logger for script
log = logging.getLogger(__name__)

# ----------------
# Template sources
# ----------------

# show system_information
sh_system_information_csv_template = env.get_template("show_system_information_csv.j2")
sh_system_information_md_template = env.get_template("show_system_information_md.j2")
sh_system_information_html_template = env.get_template("show_system_information_html.j2")


class common_setup(aetest.CommonSetup):
    """Common Setup section"""

    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        print(Panel.fit(Text.from_markup("Hang on tight - we are about to go on a [bold blue]Magic[/bold blue] [bold yellow]Carpet[/bold yellow] ride!\n\n[purple].-.\n[.-''-.,\n|  //`~\)\n(<|[/][blue]0[/][purple]|>[/][blue]0[/][purple])\n;\  _/ \\_ _\,\n__\|'._/_  \ '='-,\n/\ \    || )_///_\>>\n(  '._ T |\ | _/),-'\n'.   '._.-' /'/ |\n| '._   _.'`-.._/\n,\ / '-' |/\n[_/\-----j\n_.--.__[_.--'_\__\n/         `--'    '---._\n/ '---.  -'. .'  _.--   '.\n\_      '--.___ _;.-o     /\n'.__ ___/______.__8----'\nc-'----'[/]\n\n", justify="center")))
        testbed.connect()


# Testcase name : tc_one
class CollectInformation(aetest.Testcase):
    """Parse all the commands"""

    @aetest.test
    def parse(self, testbed, section, steps):
        """ Testcase Setup section """
        # ---------------------------------------
        # Loop over devices
        # ---------------------------------------
        for device in testbed:
            print(Panel.fit(Text.from_markup("[blue]_.---.__\n.'        `-.\n/      .--.   |\n\/  / /    |_/\n`\/|/    _(_)\n___  /|_.--'    `.   .\n\  `--' .---.     \ /|\n)   `       \     //|\n| __    __   |   '/||\n|/  \  /  \      / ||\n||  |  |   \     \  |\n\|  |  |   /        |\n__\\@/  |@ | ___ \--'\n(     /' `--'  __)|\n__>   (  .  .--' & \n/   `--|_/--'     &  |\n|                 #. |\n|                 q# |\n\              ,ad#'\n`.________.ad####'\n`#####''''''\n`&#\n&# #&\n'#ba'\n'[/]\n\nThe [bold blue]Magic[/] [bold yellow]Carpet[/] is heading into the Code of Wonders\nGenie Parsing Has Begun", justify="center",)))

            with steps.start("Parsing show system information", continue_=True) as step:
                try:
                    self.parsed_system_information = device.parse("show system information")
                except Exception as e:
                    step.failed("Could not parse it correctly\n{e}".format(e=e))

            with steps.start("Store data", continue_=True) as step:

                # Show system information
                if hasattr(self, "parsed_system_information"):
                    output_from_parsed_system_information_csv_template = (sh_system_information_csv_template.render(variable=self.parsed_system_information["system-information"]))
                    output_from_parsed_system_information_md_template = (sh_system_information_md_template.render(variable=self.parsed_system_information["system-information"]))
                    output_from_parsed_system_information_html_template = (sh_system_information_html_template.render(variable=self.parsed_system_information["system-information"]))

            # ---------------------------------------
            # Create Files
            # ---------------------------------------

            # Show system information
            if hasattr(self, "parsed_system_information"):
                with open(f"Cave_of_Wonders/Juniper/Show_System_Information/{device.alias}_show_system_information.json", "w") as fid:
                    json.dump(self.parsed_system_information, fid, indent=4, sort_keys=True)

                with open(f"Cave_of_Wonders/Juniper/Show_System_Information/{device.alias}_show_system_information.yaml", "w") as yml:
                    yaml.dump(self.parsed_system_information, yml, allow_unicode=True)

                with open(f"Cave_of_Wonders/Juniper/Show_System_Information/{device.alias}_show_system_information.csv", "w") as fh:
                    fh.write(output_from_parsed_system_information_csv_template)

                with open(f"Cave_of_Wonders/Juniper/Show_System_Information/{device.alias}_show_system_information.md", "w") as fh:
                    fh.write(output_from_parsed_system_information_md_template)

                with open(f"Cave_of_Wonders/Juniper/Show_System_Information/{device.alias}_show_system_information.html","w") as fh:
                    fh.write(output_from_parsed_system_information_html_template)

        # Goodbye Banner
        print(Panel.fit(Text.from_markup("You've made it out of the Code of Wonders on your [bold blue]Magic[/] [bold yellow]Carpet[/]!\nWhat treasures did you get?\n\n[bold yellow]_oOoOoOo_[/]\n([bold yellow]oOoOoOoOo[/])\n)`#####`(\n/         \ \n|  NETWORK  |\n|  D A T A  |\n\           /\n`=========`\n\nTo see the results of your Magic Carpet ride type\n pyats logs view\n\nWritten by John Capobianco March 2021", justify="center")))
