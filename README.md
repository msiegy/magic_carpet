# Magic Carpet

### Simply a better way; a magical way; to collect and transform network state information
![Magic Carpet](/images/magic_carpet_logo.jpg)

Powered by Genie

![Genie](/images/genie.png)

And the pyATS framework

![pyATS](/images/pyats.png)

Welcome! 

Magic Carpet is an infrastructure as code and network automation tool that transforms CLI command and REST API data, using the Cisco Genie parsers, the Cisco pyATS Python library, and Python to automatically generate, at scale, better documentation from the output; send #chatbots; #voicebots; even #phonebots!  

A Nice JSON file (command_output.json)

A Nice YAML file (command_output.yaml)

A CSV spreadsheet (command_output.csv)

A Markdown file (command_output.md)

An HTML page (comand_output.html)

Instant messages to WebEx, Slack, Discord, and others

Text-to-Speech, in over 200 languages, creating customized MP3 audio files in a human voice

Phone calls to any phone number in the world

Instantly. With the push of a button. 

## Genie and pyATS

The main Genie documentation guide:

https://developer.cisco.com/docs/genie-docs/

The main pyATS documentation guide:

https://developer.cisco.com/docs/pyats/

The Cisco's Test Automation Solution

![CTAS](/images/layers.png)

The Cisco Test Automation GitHub repository

https://github.com/CiscoTestAutomation

Here are the pyATS documentation guides on Testbed files and Device Connectivity:

Testbed and Topology Information: https://pubhub.devnetcloud.com/media/pyats/docs/topology/index.html

Device Connection: https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/quickstart/manageconnections.html

Testbed File Example: https://pubhub.devnetcloud.com/media/pyats/docs/topology/example.html

Device Connections: https://developer.cisco.com/docs/pyats/#!connection-to-devices

Secret Strings (how I encrypted the enable secret in my testbed file): https://pubhub.devnetcloud.com/media/pyats/docs/utilities/secret_strings.html

## Getting Started

**Requirements** (instructions below)

- [pyATS](https://github.com/CiscoTestAutomation)
- [Rich](https://github.com/willmcgugan/rich)

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
Activate (use) your new virtual environment (Windows):

```console
.\env\Scripts\activate
```
Download or clone the Magic Carpet repository:
```console
git clone https://github.com/automateyournetwork/magic_carpet
```
Install pyATS and Rich into your virtual environment:

```console
pip install pyats[full]
```
```console
pip install rich
```
---
If you run into any installation issues with pyATS, please see the installation guide here: https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/install/installpyATS.html

---

You're now ready to fly!

When you are finished with your pyATS session, enter the `deactivate` command to exit the python virtual environment.

## Riding the Magic Carpet

Update the `testbed/testbed.yaml` file to reflect your devices.  

Ensure SSH connectivity at from your host's CLI, and run the pyATS job:

```console
pyats run job IOS_XE_magic_carpet_job.py --testbed-file testbed/testbed.yaml
```
First - you will get onto the Magic Carpet 

![Step One](/images/Hang_On.png)

Next - Genie Magic 

![Step Two](/images/Heading_In.png)

Finally - We escape the Cave of Wonders with the network data

![Step Three](/images/We_Made_It.png)

To View the log in a Web Browser

```bash
pyats logs view
```

![Sample Log](/images/pyATS_Log_Viewer.png)


### Command Index

Cisco IOS-XE:

    show access lists

    show cdp neighbors details

    show etherchannel summary

    show interfaces status
    
    show interfaces trunk

    show inventory

    show ip arp

    show ip arp vrf {{ vrf }}

    show ip interface brief

    show issu state detail

        * 4500X IOS-XE in VSS 

    show mac address-table

    show ntp associations 

    show version

    show vrf
#### IOS-XE Tests

Tested on: 
    
    Cisco Catalyst 4500X-16 03.11.03a.E

    Cisco Catalyst 9300-48UXM Gibraltar

    Cisco Catalyst 9200-24P 16.12.03 and 17.03.02a

    Cisco Catalyst 3850-12X48U Gibraltar 16.12.04

#### The World's First Talking Network is Powered by Magic Carpet 

[![Watch the video](https://j.gifs.com/JyVY5o.gif)](https://www.youtube.com/embed/yyWnvzc0vlA)
