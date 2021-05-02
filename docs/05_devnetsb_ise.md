# Magic Carpet on ISE 

## Enable ERS

![Enable ERS](images/05_step01.png)

![Enable ERS](images/05_step02.png)

![Enable ERS](images/05_step03.png)

![Enable ERS](images/05_step04.png)

### Run Magic Carpet on ISE 

```console
pyats run job DevNet_Sandbox_ISE_magic_carpet_job.py
```

First - you will get onto the Magic Carpet

![Step One](/images/Hang_On.png)

Next - Genie Magic

![Step Three](/images/Heading_In.png)

We head into the cloud !

![Step Four](/images/CloudMonkey.PNG)

All of the CLI and API JSON is magically transformed

![Step Five](/images/SaveFiles.PNG)

Finally - We escape the Cave of Wonders with the network data

![Step Six](/images/We_Made_It.png)

```bash
cd Cave_of_Wonders/Cisco/DevNet_Sandbox/ISE

ls 
```

To view the pyATS log in a web browser Locally

```bash
pyats logs view
```

To view the pyATS log in a web browser remotely

```bash
pyats logs view --host 0.0.0.0 --port 8080 -v
```

![Sample Log](/images/pyATS_Log_Viewer.png)
