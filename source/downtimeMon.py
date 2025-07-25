from collections import deque
from datetime import datetime, timezone, timedelta
import os
import time

import psPythonProcs

_dtMonVer = '1.0.1'

try:
    if psPythonProcs.libExists() != True:
        print("psPythonProcs not available - exiting (1)")
        exit(100)
except:
    print("psPythonProcs not available - exiting (2)")
    exit(100)

#--------------------------------------------------------------------------
# --- CONFIGURATION
#--------------------------------------------------------------------------
_scriptDir = os.path.dirname(os.path.abspath(__file__))
if not psPythonProcs.objectPopulated_String("_scriptDir", _scriptDir):
    print("_scriptDir not populated - exiting")
    exit(100)

_appSettings = psPythonProcs.PsPythonSettingsFile(_scriptDir + "/downtimeMon.settings.json")
if not psPythonProcs.objectExists("_appSettings", _appSettings):
    print("_appSettings not populated - exiting")
    exit(100)

_lastExecutionFile = _appSettings.setting_Get("lastExecutionFile")
if not psPythonProcs.objectPopulated_String("_lastExecutionFile", _lastExecutionFile):
    print("_lastExecutionFile not populated - exiting")
    exit(100)

_logsDir = _appSettings.setting_Get("logsDirectory")
if not psPythonProcs.objectPopulated_String("_logsDir", _logsDir):
    print("_logsDir not populated - exiting")
    exit(100)

_executionLogFile = _logsDir + "/executions.log"
_downtimeLogFile = _logsDir + "/downtime.log" 

_intervalSecs =int(_appSettings.setting_Get("testIntervalSecs"))  # Execute every n seconds
if not psPythonProcs.objectPopulated_Int("_intervalSecs", _intervalSecs):
    print("_intervalSecs not populated - exiting")
    exit(100)

_executionLogLen = int(_appSettings.setting_Get("executionLogLen"))
if not psPythonProcs.objectPopulated_Int("_executionLogLen", _executionLogLen):
    print("_executionLogLen not populated - exiting")
    exit(100)


statusMsg = 'Launching downtimeMon (v' + _dtMonVer + ')... \n'
statusMsg += '   Execution Directory: "' + _scriptDir + '"\n'
statusMsg += '   Last execution file: "' + str(_lastExecutionFile) + '"\n'
statusMsg += '   Executions log file: "' + str(_executionLogFile) + '"\n'
statusMsg += '   Downtime log file: "' + str(_downtimeLogFile) + '" \n'
statusMsg += '   Test interval seconds: ' + str(_intervalSecs)  + '\n'
statusMsg += '   Execution log len: ' + str(_executionLogLen)
print(statusMsg)


#--------------------------------------------------------------------------
# --- METHODS
#--------------------------------------------------------------------------

#def script_is_running(scriptPath):
#    for q in psutil.process_iter():
#        if q.name().startswith('python'):
#            if len(q.cmdline()) > 1 and scriptPath in q.cmdline() and q.pid != os.getpid():
#                print(f"'{scriptPath}' Process is already running")
#                return True
#    return False


def check_for_downtime(executionTs):
    lastExecContent = '';
    if os.path.exists(_lastExecutionFile):
        with open(_lastExecutionFile, 'r') as f:
            lastExecContent = f.read()
            if len(lastExecContent.strip()) > 0:
                lsc = datetime.fromisoformat(lastExecContent.strip())
                lsc.replace(tzinfo=timezone.utc)
                if lsc + timedelta(seconds=(_intervalSecs + 2)) < executionTs:
                    return True, lsc
    return False, None

        
def log_downtime(lastStatusTs):
    currTs = datetime.now(timezone.utc)
    diff = currTs - lastStatusTs
    logVal = '{ "currentTimestamp":"' + datetime.isoformat(currTs) + '", "lastExecutionFileEntry":"' + datetime.isoformat(lastStatusTs) + '", "down_hours":' + format(diff.total_seconds()/3600, '.2f')  + ', "down_minutes":' + format(diff.total_seconds()/60, '.2f') + ', "test_interval_secs":' + str(_intervalSecs) + '}'
    with open(_downtimeLogFile, 'a') as f:
        f.write(logVal + "\n")


def log_execution(executionTs):
    try:
        if os.path.exists(_executionLogFile):
            with open(_executionLogFile, 'r') as f:
                # Use deque with maxlen to efficiently store only the last n lines
                last_lines = deque(f, maxlen=_executionLogLen-1)

            # Overwrite the original file with the retained lines
            with open(_executionLogFile, 'w') as f:
                for line in last_lines:
                    f.write(line)

        if os.path.exists(_executionLogFile):
            with open(_executionLogFile, 'a') as f:
                f.write(datetime.isoformat(executionTs) + "\n")
        else:
            with open(_executionLogFile, 'w') as f:
                f.write(datetime.isoformat(executionTs) + "\n")

    except FileNotFoundError:
        print(f"Error: File not found at " + _executionLogFile)
    except Exception as e:
        print(f"An error occurred: {e}")

    
def store_ExecutionTs(executionTs):   
    # Delete the file, if existing   
    #if os.path.exists(_lastExecutionFile):
    #    os.remove(_lastExecutionFile)
    with open(_lastExecutionFile, 'w') as f:
        f.write(executionTs.isoformat())    


#--------------------------------------------------------------------------
# --- MAIN LOGIC
#--------------------------------------------------------------------------

#if script_is_running(_scriptDir + '/downtimeMon.py'):
#    sys.exit('Aborting startup... Already running')

while True:
    currTs = datetime.now(timezone.utc)    
    downtime, lastExecutionTs = check_for_downtime(currTs)
    if downtime == True:
        log_downtime(lastExecutionTs)
    store_ExecutionTs(currTs)
    log_execution(currTs)
    nextExec =  currTs + timedelta(seconds=_intervalSecs)
    sleepSecs = (nextExec - datetime.now(timezone.utc)).total_seconds()
    #print(f"   sleepSecs: {str(sleepSecs)}")
    if sleepSecs > 0:
        time.sleep(sleepSecs)
	
