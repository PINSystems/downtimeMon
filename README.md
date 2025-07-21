# downtimeMon
Python system downtime tracking.

The use case that spawned downtimeMon is as a home appliance.  After being on vacation, we returned to a beeping freezer and flashing clocks. I could determine what time of day the power turned back on, but not how long it had been off.  Was it off for two hours, 14 hours, 26 hours, etc.?  I was originally thinking of building an AC powered appliance, then realized I have at least one.  When the power go es off, I have a Raspberry Pi that isn't on a UPS, so it shuts down and starts back up when power is available. 

donwtimeMon is a simple Python based service that executes every n seconds. When it executes, it reads the last execution time and conmpares it to the current time.  If the difference in timestamps is more than the "interval" setting (+ two seconds), an outage has been encountered. If an outage is encountered, it's logged. Before sleeping, the current execution time is stored for the next execution.

You can review data via the downtimeMon http service or the logs.
Default URL:  http://<IpAddress>:8899
Default Logs Folder:  /etc/downtimeMon/logs
The http service reads the logs and presents the data.

downtimeMon requires very few resource. It should operate properly on any Raspberry Pi or linux based machine with Python installed.

Installation -------------------------
1) Log in as a sudo user.
2) Create a directory in the home directory.
3) Copy/transfer the distribution files to the directory created in step 2
4) Open a shell, change to the directory fronm step 2
5) Execute:  sudo python3 downtimeMon.install.py
6) After execution is verified, the folder created in step 2 can be deleted

The installation process -------------------
a) first makes sure the downtimeMon services aren't running
b) Then it creates the following folders, if they don't already exist:
    /etc/downtimeMon
    /etc/downtimeMon/logs
c) It then removes any/all files from /etc/downtimeMon/
d) Then it copies the following files to /etc/downtimeMon/
    downtimeMon.py
    downtimeMonServer.py
    downtimeMon.info.txt
e) Then it copies the following files to /etc/systemd/system/
    downtimeMon.service
    downtimeMonServer.service
f) Then it registers and starts the services:
    downtimeMon
    downtimeMonServer
