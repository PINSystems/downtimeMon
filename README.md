# downtimeMon
### Python system downtime tracking.

The use case that spawned downtimeMon is as a home appliance.  After being on vacation, we returned to a beeping freezer and flashing clocks. I could determine what time of day the power turned back on, but not how long it had been off.  Was it off for two hours, 14 hours, 26 hours, etc.? Do we need to throw food out? I was originally thinking of building an AC powered appliance (analog clock/calendar), then realized I have at least one.  I have a Raspberry Pi that isn't on a UPS, so it shuts down during a power outage and starts back up when power is available. Enter downimeMon.

donwtimeMon is a Python based service that executes every n seconds. When it executes, it reads the last execution time and compares it to the current time.  If the difference is more than the "interval" setting (+ two seconds), an outage has been encountered. If an outage is encountered, it's logged. Then the current execution time is stored for the next execution.

You can review data via the downtimeMon http service or the logs.  
Default URL:  http://[IpAddress]:8899  
Default Logs Folder:  /etc/downtimeMon/logs  
The http service merely reads the log files and presents the data.  

downtimeMon requires very few resources. It should operate properly on any Raspberry Pi or linux based machine with Python3 installed.

### Installation -------------------------
1) Log in as a sudo user.  
2) Create a directory in the home directory.  
3) Copy/transfer the distribution files to the directory created in step 2  
4) If changing any app settings, they can be found in downtimeMon.settings.json.  
   This file is used by downtimeMon.install.py, downtimeMon.py and downtimeMonServer.py  
   Settings should be updated before executing the install script as the "installDir" setting is used to build the service files.  
   Default Setting Values:  
     "installDir":"/etc/downtimeMon",  
     "logsDirectory": "/etc/downtimeMon/logs",  
     "lastExecutionFile": "/etc/downtimeMon/lastExecution",  
     "testIntervalSecs":"300",  
     "executionLogLen": "25",  
     "serverHttpPort": "8899"  
5) Open a shell, change to the directory fronm step 2  
6) Execute:  sudo python3 downtimeMon.install.py  
7) After execution is verified, the folder created in step 2 can be deleted  
  
  
**The installation process (assuming default setting values):**
- Makes sure the downtimeMon services aren't running  
- Creates the following folders, if they don't already exist:  
&nbsp;&nbsp;    [installDir]   
&nbsp;&nbsp;    [logsDirectory]   
- Removes any/all files from [installDir]  
- Copies the following files to [installDir]  
&nbsp;&nbsp;    downtimeMon.py  
&nbsp;&nbsp;    downtimeMon.history.txt  
&nbsp;&nbsp;    downtimeMon.settings.json  
&nbsp;&nbsp;    downtimeMonServer.py  
&nbsp;&nbsp;    psPythonProcs.py  
- Generates service files from the following and places the service files in /etc/systemd/system/  
&nbsp;&nbsp;    downtimeMon.service.template  
&nbsp;&nbsp;    downtimeMonServer.service.template  
- Registers and starts the services:  
&nbsp;&nbsp;    downtimeMon  
&nbsp;&nbsp;    downtimeMonServer  

### downtimeMon Dashboard...  
<img width="450" alt="downtimeMon_Dashboard" src="https://github.com/user-attachments/assets/b78dd73d-338c-442b-b719-10dbbb6187ae" />

