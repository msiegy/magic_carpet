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

template_dir = 'templates/f5'
env = Environment(loader=FileSystemLoader(template_dir))

print(Panel.fit(Text.from_markup("Hang on tight - we are about to go on a [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/bold yellow][/blink] ride!\n\n[purple].-.\n[.-''-.,\n|  //`~\)\n(<|[/][blue]0[/][purple]|>[/][blue]0[/][purple])\n;\  _/ \\_ _\,\n__\|'._/_  \ '='-,\n/\ \    || )_///_\>>\n(  '._ T |\ | _/),-'\n'.   '._.-' /'/ |\n| '._   _.'`-.._/\n,\ / '-' |/\n[_/\-----j\n_.--.__[_.--'_\__\n/         `--'    '---._\n/ '---.  -'. .'  _.--   '.\n\_      '--.___ _;.-o     /\n'.__ ___/______.__8----'\nc-'----'[/]\n\n",justify="center")))

# ---------------------------------------
# Loop over devices
# ---------------------------------------

with open("testbed/testbed_f5.yaml") as stream:
    testbed = yaml.safe_load(stream)


# ---------------------------------------
# API Get Token
# ---------------------------------------

for device,value in testbed['devices'].items():
    api_username = testbed["devices"][device]["credentials"]["default"]["username"]
    api_password = testbed["devices"][device]["credentials"]["default"]["password"]
    device_alias = testbed["devices"][device]["alias"]
    f5_token_raw = requests.post("https://%s/mgmt/shared/authn/login" % device, json={"username":"%s" % api_username, "password": "%s" % api_password,"loginprovidername": "tmos"}, verify=False)
    f5_token_json = f5_token_raw.json()
    f5_usable_token = f5_token_json["token"]["token"]

headers={"X-F5-Auth-Token":f5_usable_token}

# ---------------------------------------
# F5 Virtual Servers
# ---------------------------------------
for device in testbed['devices']:
    raw_vs = requests.get("https://%s/mgmt/tm/ltm/virtual" % device_alias, headers=headers, verify=False)
    vs_json = raw_vs.json()
    vs_template = env.get_template('virtual_servers.j2')

# ---------------------------------------
# Generate CSV / MD / HTML / Mind Maps
# ---------------------------------------
    with open("Cave_of_Wonders/F5/%s_virtual_servers.json" % device_alias, "w") as fid:
        json.dump(vs_json, fid, indent=4, sort_keys=True)

    with open("Cave_of_Wonders/F5/%s_virtual_servers.yaml" % device_alias, "w") as yml:
        yaml.dump(vs_json, yml, allow_unicode=True)

    for filetype in filetype_loop:
        parsed_output_vs = vs_template.render(to_parse_vs=vs_json['items'],filetype_loop_jinja2=filetype)

        with open("Cave_of_Wonders/F5/%s_virtual_servers.%s" % (device_alias,filetype), "w") as fh:
            fh.write(parsed_output_vs) 
                    
    os.system("markmap Cave_of_Wonders/F5/%s_virtual_servers.md --output Cave_of_Wonders/F5/%s_virtual_servers_mind_map.html" % (device_alias,device_alias))

# ---------------------------------------
# You Made It 
# ---------------------------------------
    print(Panel.fit(Text.from_markup("[blue]_.---.__\n.'        `-.\n/      .--.   |\n\/  / /    |_/\n`\/|/    _(_)\n___  /|_.--'    `.   .\n\  `--' .---.     \ /|\n)   `       \     //|\n| __    __   |   '/||\n|/  \  /  \      / ||\n||  |  |   \     \  |\n\|  |  |   /        |\n__\\@/  |@ | ___ \--'\n(     /' `--'  __)|\n__>   (  .  .--' & \n/   `--|_/--'     &  |\n|                 #. |\n|                 q# |\n\              ,ad#'\n`.________.ad####'\n`#####''''''\n`&#\n&# #&\n'#ba'\n'[/]\n\nThe [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/][/blink] is heading into the [bold cyan]Cave of Wonders[/bold cyan]\n\n[bold blue]Genie[/bold blue] Parsing Has Begun",justify="center")))

    # For loop done - We're done here!
    # Copy all Wonders to runinfo so it is visible in the logviewer
    # Not working - but should work next week - This would allow to 
    # see all the Wonders in the brower too!
    # shutil.copytree('Wonders', os.path.join(self.parameters['runinfo_dir'], 'Wonders'))

    # Goodbye Banner
    print(Panel.fit(Text.from_markup("You've made it out of the [bold orange]Cave of Wonders[/bold orange] on your [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/][/blink]!\n[green]What treasures did you get?[/green]\n\n[bold yellow]_[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]_[/]\n([bold yellow][blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink]O[blink]o[/blink][/])\n)`#####`(\n/         \ \n|  [bold green]NETWORK[/bold green]  |\n|  [bold green]D A T A[/bold green]  |\n\           /\n`=========`\n\n\n\nYour Network Data can be found in the [bold cyan]Cave of Wonders[/bold cyan]\n\nType cd [bold cyan]Cave_of_Wonders[/bold cyan]\n\nTo see the log of your [blink][bold blue]Magic[/bold blue][/blink] [blink][bold yellow]Carpet[/][/blink] ride \nType [bold red]pyats logs view[/bold red]\n\nWritten by John Capobianco March 2021",justify="center")))
