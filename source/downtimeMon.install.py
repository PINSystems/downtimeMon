import os
import shutil
import subprocess
import sys
import time 

import psPythonProcs

try:
    if psPythonProcs.libExists() != True:
        print("psPythonProcs not available - exiting (1)")
        exit(100)
except:
    print("psPythonProcs not available - exiting (2)")
    exit(100)

_scriptDir = os.path.dirname(os.path.abspath(__file__))
if not psPythonProcs.objectPopulated_String("_scriptDir", _scriptDir):
    print("_scriptDir not populated - exiting")
    exit(100)

_appSettings = psPythonProcs.PsPythonSettingsFile(_scriptDir + "/downtimeMon.settings.json")
if not psPythonProcs.objectExists("_appSettings", _appSettings):
    print("_appSettings not populated - exiting")
    exit(100)

_installDir = _appSettings.setting_Get("installDir")
if not psPythonProcs.objectPopulated_String("_installDir", _installDir):
    print("_installDir not populated - exiting")
    exit(100)

_logsDir = _appSettings.setting_Get("logsDirectory")
if not psPythonProcs.objectPopulated_String("_logsDir", _logsDir):
    print("_logsDir not populated - exiting")
    exit(100)

result=False

statusMsg = 'Launching downtimeMon installation... \n' 
statusMsg += '   Installation directory: "' + _installDir + '"\n'
statusMsg += '   Logs directory: "' + _logsDir + '"\n'
print(statusMsg)



#----------------------------------------------------
# --- Stop the services
#----------------------------------------------------
psPythonProcs.service_stop("downtimeMon")
psPythonProcs.service_stop("downtimeMonServer")


#----------------------------------------------------
# --- Create the reqiuired directories
#----------------------------------------------------
result = psPythonProcs.dir_create(_installDir)
if not result:
    sys.exit('Aborting install!')

result = psPythonProcs.dir_create(_logsDir)
if not result:
    sys.exit('Aborting install!')


#----------------------------------------------------
# --- Remove prior version files
#----------------------------------------------------
for filename in os.listdir(_installDir):
   file_path = os.path.join(_installDir, filename)
   if os.path.isfile(file_path):
      os.remove(file_path)


#----------------------------------------------------
# --- Copy the required files
#----------------------------------------------------

result = psPythonProcs.file_copy('./downtimeMon.settings.json', _installDir + '/downtimeMon.settings.json')
if not result:
    sys.exit('Aborting install!')

result = psPythonProcs.file_copy('./psPythonProcs.py', _installDir + '/psPythonProcs.py')
if not result:
    sys.exit('Aborting install!')

result = psPythonProcs.file_copy('./downtimeMon.py', _installDir + '/downtimeMon.py')
if not result:
    sys.exit('Aborting install!')

result = psPythonProcs.file_copy('./downtimeMonServer.py', _installDir + '/downtimeMonServer.py')
if not result:
    sys.exit('Aborting install!')

result = psPythonProcs.file_copy('./downtimeMon.history.txt', _installDir + '/downtimeMon.history.txt')
if not result:
    sys.exit('Aborting install!')

# Prepare and copy/place the downtimeMon.service file
#--------------------------------------------------------------------
svcFileContent = ""
with open('./downtimeMon.service.template', 'r') as file:
    svcFileContent = file.read()
svcFileContent = svcFileContent.replace("<<<installDir>>>", _installDir)
with open('./downtimeMon.service', 'w') as file:
    file.write(svcFileContent)
# Copy the downtimeMon.service file
result = psPythonProcs.file_copy('./downtimeMon.service', '/etc/systemd/system/downtimeMon.service')
if not result:
    sys.exit('Aborting install!')

# Prepare and copy/place the downtimeMonServer.service file
#--------------------------------------------------------------------
svcFileContent = ""
with open('./downtimeMonServer.service.template', 'r') as file:
    svcFileContent = file.read()
svcFileContent = svcFileContent.replace("<<<installDir>>>", _installDir)
with open('./downtimeMonServer.service', 'w') as file:
    file.write(svcFileContent)
# Copy the downtimeMonServer.service file
result = psPythonProcs.file_copy('./downtimeMonServer.service', '/etc/systemd/system/downtimeMonServer.service')
if not result:
    sys.exit('Aborting install!')


#----------------------------------------------------
# --- Start the services
#----------------------------------------------------

# --- Update systemd internal data
psPythonProcs.service_defs_reload()

# --- Enable the MONITOR service
psPythonProcs.service_enable("downtimeMon.service")

# --- Start the MONITOR service
psPythonProcs.service_start("downtimeMon.service")

# --- Enable the SERVER service
psPythonProcs.service_enable("downtimeMonServer.service")

# --- Start the SERVER service
psPythonProcs.service_start("downtimeMonServer.service")


#----------------------------------------------------
# We're done!
#----------------------------------------------------

print(f"\nInstallation complete. \nRetrieving service status...\n")

time.sleep(3)
statusText = psPythonProcs.service_status("downtimeMon.service")
print(f'downtimeMon.service status: \n' + statusText)
statusText = psPythonProcs.service_status("downtimeMonServer.service")
print(f'downtimeMonServer.service status: \n' + statusText)
