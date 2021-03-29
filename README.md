# Magic Carpet

### Simply a better way; a magical way; to collect and transform network state information

![Magic Carpet](/images/magic_carpet_logo.jpg)

Powered by Genie

![Genie](/images/genie.png)

And the pyATS framework

![pyATS](/images/pyats.png)

Featuring

![Markmap](/images/MarkMapLogo.PNG)

Welcome!

Magic Carpet is an infrastructure as code and network automation tool that transforms CLI command and REST API data, using the Cisco Genie parsers, the Cisco pyATS Python library, and Python to automatically generate, at scale, better documentation from the output; send #chatbots; #voicebots; even #phonebots!  

A Nice JSON file (command_output.json)

A Nice YAML file (command_output.yaml)

A CSV spreadsheet (command_output.csv)

A Markdown file (command_output.md)

An HTML page (comand_output.html)

An interactive HTML Mind Map (command_output_mind_map.html)

Instant messages to WebEx, Slack, Discord, and others

Text-to-Speech, in over 200 languages, creating customized MP3 audio files in a human voice

Phone calls to any phone number in the world

Instantly. With the push of a button.

## Genie and pyATS

The main Genie documentation guide:

<https://developer.cisco.com/docs/genie-docs/>

The main pyATS documentation guide:

<https://developer.cisco.com/docs/pyats/>

The Cisco's Test Automation Solution

![CTAS](/images/layers.png)

The Cisco Test Automation GitHub repository

<https://github.com/CiscoTestAutomation>

Here are the pyATS documentation guides on Testbed files and Device Connectivity:

Testbed and Topology Information: <https://pubhub.devnetcloud.com/media/pyats/docs/topology/index.html>

Device Connection: <https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/quickstart/manageconnections.html>

Testbed File Example: <https://pubhub.devnetcloud.com/media/pyats/docs/topology/example.html>

Device Connections: <https://developer.cisco.com/docs/pyats/#!connection-to-devices>

Secret Strings (how I encrypted the enable secret in my testbed file): <https://pubhub.devnetcloud.com/media/pyats/docs/utilities/secret_strings.html>

## Getting Started

**Requirements** (instructions below)

- [pyATS](https://github.com/CiscoTestAutomation)
- [Rich](https://github.com/willmcgugan/rich)
- [markmap (CLI)](https://markmap.js.org/)

**Virtual Environment**

We recommend running Magic Carpet in a Python [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) while testing or developing.  This will help keep your host system clean and allow you to have multiple environments to try new things.  If you are not using a virtual environment, start at the download/clone step below.

You will also need Python 3, pip, and venv installed on your host system.

In your project directory, create your virtual environment

```console
python3 -m venv env
```

Activate (use) your new virtual environment (Linux):

```console
source env/bin/activate
```

Download or clone the Magic Carpet repository:

```console
git clone https://github.com/automateyournetwork/magic_carpet
```

Install pyATS, Rich, and markmap into your environment:

```console
pip install pyats[full]
```

```console
pip install rich
```

```console
sudo apt update
sudo apt install npm
sudo npm install markmap-cli -g
```

---
If you run into any installation issues with pyATS, please see the installation guide here: <https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/install/installpyATS.html>

---

You're now ready to fly!

When you are finished with your pyATS session, enter the `deactivate` command to exit the python virtual environment.

# Riding the Magic Carpet

How to update the appropriate `testbed/testbed_*.yaml` file to reflect your device inventory and configuration:

![Testbed - Routers](/images/testbed_routers.PNG)

    Devices:

        4500: <-- Update to your router hostname (MUST MATCH HOSTNAME)

            alias: <-- Update your alias; this can be the hostname or any friendly name you want

            type: <-- This should be "router" for L3 routers with ARP tables and VRFs and such 

            platform: <-- Your Catalyst IOS-XE Platform

            username: <-- Your Cisco device username

            password: <-- Your Enable Secret; It is strongly recommended to follow the "Secret Strings" link to encrypt your secrets

            ip: <-- The management IP address of your router 

        Copy & Paste and make each device unique to scale this up to many routers

![Testbed - Switches](/images/testbed_switches.PNG)

    Devices:

        3850: <-- Update to your switch hostname (MUST MATCH HOSTNAME)
        9300: <-- Update to your switch hostname (MUST MATCH HOSTNAME)

            alias: <-- Update your alias; this can be the hostname or any friendly name you want

            type: <-- This should be "switch" for L2 switches without ARP tables or VRFs but features like PoE 

            platform: <-- Your Catalyst IOS-XE Platform

            username: <-- Your Cisco device username

            password: <-- Your Enable Secret; It is strongly recommended to follow the "Secret Strings" link to encrypt your secrets

            ip: <-- The management IP address of your router 

        Copy & Paste and make each device unique to scale this up to many routers    

Ensure SSH connectivity at from your host's CLI, and run the pyATS job:

Cisco IOS-XE:

```console
pyats run job IOS_XE_magic_carpet_job.py --testbed-file testbed/testbed_ios_xe.yaml
```

Cisco DevNet Sandbox for CSR1000v

```console
pyats run job DevNet_Sandbox_CSR_magic_carpet_job.py --testbed-file testbed/testbed_DevNet_CSR1000v_Sandbox.yaml
```

JunOS 17 / 18 / 19:

```console
pyats run job JUNOS_magic_carpet_job.py --testbed-file testbed/testbed_juniper.yaml
```

F5 BIG-IP:

```console
python3 F5_magic_carpet.py
```

First - you will get onto the Magic Carpet

![Step One](/images/Hang_On.png)

Next - Genie Magic

![Step Two](/images/Heading_In.png)

Finally - We escape the Cave of Wonders with the network data

![Step Three](/images/We_Made_It.png)

```bash
cd Cave_of_Wonders

ls 
```

To view the pyATS log in a web browser Locally

```bash
pyats logs view
```

To view the pyATTS log in a web browser remotely

```bash
pyats logs view --host 0.0.0.0 --port 8080 -v
```

![Sample Log](/images/pyATS_Log_Viewer.png)

# Explore your Wonders!

Here is an example of just one of the Wonders you will find: the `show ip route` command!

Here is what a Global Routing Table looks like in JSON:

![JSON_Output](/images/CaveOfWonders_IP_Route_JSON.PNG)

The same routing table, but in YAML:

![YAML_Output](/images/CaveOfWonders_IP_Route_YAML.PNG)

The JSON and YAML outputs are incredible representations of the routing table and can be used for further pyATS testing or data modeling.

"Business-ready" documentation includes the incredibly powerful and versatile Comma-Separated Values (csv) spreadsheet format.

![CSV_Output](/images/CaveOfWonders_IP_Route_CSV.PNG)

Markdown, the format this README file is written in, can also be used to express the data in a lightweight format that renders nicely in modern browsers.

![MD_Output](/images/CaveOfWonders_IP_Route_MD.PNG)

What about a full-blown HTML webpage? Magic Carpet also creates at least one of these per command.

![HTML_RAW_Output](/images/CaveOfWonders_IP_Route_HTML_Raw.PNG)

Which renders nicely like this in your browser:

![HTML_Rendered_Output](/images/CaveOfWonders_IP_Route_HTML_Rendered.PNG)

Another HTML page, an interactive mindmap, is also created from the Markdown file!

![Mind_Map_Output](/images/CaveOfWonders_IP_Route_Mind_Map.PNG)

To launch a Python web server and make the Cave of Wonders available in a browser, where you can view the HTML pages:

Launch a local web server available on the same host:

```bash
cd Cave_of_Wonders
pushd;  python3 -m http.server --bind 127.0.0.1 8888; popd;
```

Launch your web browser and visit

<http://127.0.0.1:8888/>

Launch a local web server available to remote hosts:

```bash
cd Cave_of_Wonders
pushd;  python3 -m http.server --bind 0.0.0.0 8888; popd;
```

Launch your web browser and visit

`http://{{ your server IP }}:8888/`

### Supported Command Index

Cisco IOS-XE:

    show access lists

    show access session

    show access session interface {{ interface }} detail

    show authentication sessions

    show authentication session interface {{ interface }} detail

    show cdp neighbors details

    show etherchannel summary

    show interfaces status
    
    show interfaces trunk

    show inventory

    show ip arp

    show ip arp vrf {{ vrf }}

    show ip interface brief

    show ip ospf

    show ip ospf database

    show ip ospf interface

    show ip ospf neighbor

    show ip ospf neighbor detail

    show ip route

    show ip route vrf {{ vrf }}

    show issu state detail

        * 4500X IOS-XE in VSS 

    show mac address-table

    show ntp associations

    show power inline

    show version

    show vrf

JunOS:

    show_system_information

F5 BIG-IP

    mgmt/tm/ltm/virtual

#### Cross Platform Tests

Tested on:

    Cisco:

        Cisco Catalyst 4500X-16 03.11.03a.E

        Cisco Catalyst 9300-48UXM Gibraltar

        Cisco Catalyst 9200-24P 16.12.03 and 17.03.02a

        Cisco Catalyst 3850-12X48U Gibraltar 16.12.04

        Cisco CSR1000v

        Cisco IOSv

    Juniper:

        JunOS 17, 18, 19

    F5: 

        i2600 REST API

# Test it yourself in the Cisco DevNet Always-On Sandbox

Vist https://devnetsandbox.cisco.com/RM/Topology

Sign-in

Int he top left - search for "CSR"

![DevNet_Search](/images/01_DevNet_Search.PNG)

Select your Sandbox

![DevNet_Select](/images/02_DevNet_Select.PNG)

Follow the VPN Instructions closely 

![DevNet_VPN_Instructions](/images/03_DevNet_VPN_Instructions.PNG)

Download the AnyConnect VPN Client

https://developer.cisco.com/site/sandbox/anyconnect/

The installation guide is available here

https://devnetsandbox.cisco.com/Docs/VPN_Access/AnyConnect_Installation_Guide.pdf

Reserve the Lab in the top right of the browser

![DevNet_Reserve](/images/04_DevNet_Reserve.PNG)

The lab will take approximately 15 - 20 minutes to initialize. When it is ready you will receive an e-mail containing:

The FQDN of the VPN address to connect to 

Your VPN username 

Your VPN password

Establish your VPN connection

![DevNet_VPN_Connected](/images/05_DevNet_VPN_Connected.PNG)

Next confirm the CSR1000v IP Address, Username, and Password in your sandbox

![DevNet_VPN_Host_Info](/images/06_DevNet_Host_Info.PNG)

Matches the details inside testbed/testbed_DevNet_CSR1000v_Sandbox.yaml

![DevNet_Testbed](/images/07_DevNet_Testbed.PNG)

Run Magic Carpet! 

```console
pyats run job DevNet_Sandbox_CSR_magic_carpet_job.py --testbed-file testbed/testbed_DevNet_CSR1000v_Sandbox.yaml
```
# The World's First Talking Network is Powered by Magic Carpet

[![Watch the video](https://j.gifs.com/JyVY5o.gif)](https://www.youtube.com/embed/yyWnvzc0vlA)
