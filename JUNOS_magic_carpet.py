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
from jinja2 import Environment, FileSystemLoader

template_dir = "templates/juniper"
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# Get logger for script
# ----------------
log = logging.getLogger(__name__)

# ----------------
# Filetypes 
# ----------------

filetype_loop = ["csv","md","html"]

class common_setup(aetest.CommonSetup):
    """Common Setup section"""

    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        print(Panel.fit(Text.from_markup("Hang on tight - we are about to go on a [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/bold yellow][/blink] ride!\n\n[purple].-.\n[.-''-.,\n|  //`~\)\n(<|[/][blue]0[/][purple]|>[/][blue]0[/][purple])\n;\  _/ \\_ _\,\n__\|'._/_  \ '='-,\n/\ \    || )_///_\>>\n(  '._ T |\ | _/),-'\n'.   '._.-' /'/ |\n| '._   _.'`-.._/\n,\ / '-' |/\n[_/\-----j\n_.--.__[_.--'_\__\n/         `--'    '---._\n/ '---.  -'. .'  _.--   '.\n\_      '--.___ _;.-o     /\n'.__ ___/______.__8----'\nc-'----'[/]\n\n",justify="center")))
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
            print(Panel.fit(Text.from_markup("[blue]_.---.__\n.'        `-.\n/      .--.   |\n\/  / /    |_/\n`\/|/    _(_)\n___  /|_.--'    `.   .\n\  `--' .---.     \ /|\n)   `       \     //|\n| __    __   |   '/||\n|/  \  /  \      / ||\n||  |  |   \     \  |\n\|  |  |   /        |\n__\\@/  |@ | ___ \--'\n(     /' `--'  __)|\n__>   (  .  .--' & \n/   `--|_/--'     &  |\n|                 #. |\n|                 q# |\n\              ,ad#'\n`.________.ad####'\n`#####''''''\n`&#\n&# #&\n'#ba'\n'[/]\n\nThe [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/][/blink] is heading into the [bold cyan]Cave of Wonders[/bold cyan]\n\n[bold blue]Genie[/bold blue] Parsing Has Begun",justify="center")))

            with steps.start("Parsing show system information", continue_=True) as step:
                try:
                    self.parsed_system_information = device.parse("show system information")
                except Exception as e:
                    step.failed("Could not parse it correctly\n{e}".format(e=e))

            with steps.start("Store data", continue_=True) as step:

                # Show system information
                if hasattr(self, "parsed_system_information"):
                    sh_system_information_csv_template = env.get_template("show_system_information.j2")

                with open(f"Cave_of_Wonders/Juniper/Show_System_Information/{device.alias}_show_system_information.json", "w") as fid:
                    json.dump(self.parsed_system_information, fid, indent=4, sort_keys=True)

                with open(f"Cave_of_Wonders/Juniper/Show_System_Information/{device.alias}_show_system_information.yaml", "w") as yml:
                    yaml.dump(self.parsed_system_information, yml, allow_unicode=True)

                for filetype in filetype_loop:
                    parsed_output_type = (sh_system_information_csv_template.render(variable=self.parsed_system_information["system-information"],filetype_loop_jinja2=filetype))

                    with open(f"Cave_of_Wonders/Juniper/Show_System_Information/{device.alias}_show_system_information.{filetype}", "w") as fh:
                        fh.write(parsed_output_type)

                os.system("markmap Cave_of_Wonders/Juniper/Show_System_Information/{device.alias}_show_system_information.md --output Cave_of_Wonders/Juniper/Show_System_Information/{device.alias}_show_system_information.html")

        # Goodbye Banner
        print(Panel.fit(Text.from_markup("You've made it out of the [bold orange]Cave of Wonders[/bold orange] on your [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/][/blink]!\n[green]What treasures did you get?[/green]\n\n[bold yellow]_[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]_[/]\n([bold yellow][blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink][/])\n)`#####`(\n/         \ \n|  [bold green]NETWORK[/bold green]  |\n|  [bold green]D A T A[/bold green]  |\n\           /\n`=========`\n\n\n\nYour Network Data can be found in the [bold cyan]Cave of Wonders[/bold cyan]\n\nType cd [bold cyan]Cave_of_Wonders[/bold cyan]\n\nTo see the log of your [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/][/blink] ride \nType [bold red]pyats logs view[/bold red]\n\nWritten by John Capobianco March 2021",justify="center")))
