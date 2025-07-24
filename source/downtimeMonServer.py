from http.server import BaseHTTPRequestHandler
import json
import os
import http.server
import socketserver

import psPythonProcs

_dtMonVer = '1.0.0'

_scriptDir = os.path.dirname(os.path.abspath(__file__))
_appSettings = psPythonProcs.PsPythonSettingsFile(_scriptDir + "/downtimeMon.settings.json")

_executionLogFile =  _appSettings.setting_Get("logsDirectory") + "/executions.log"
_downtimeLogFile = _appSettings.setting_Get("logsDirectory") + "/downtime.log" 
_serverPort = int(_appSettings.setting_Get("serverHttpPort"))

statusMsg = 'Launching downtimeMonServer... \n'
statusMsg += '   Executions log file: "' + _executionLogFile + '" \n'
statusMsg += '   Downtime log file: "' + _downtimeLogFile + '" \n'
statusMsg += '   Server port: ' + str(_serverPort)
print(statusMsg)


def prep_response_Dashboard():
    downtimeData = load_downtimeFileContent()
    executionData = load_executionFileContent()

    ret = "<HTML>"
    ret += "    <HEAD>"        
    ret += "        <meta name='viewport' content='width=device-width, initial-scale=.9'>"
    ret += "        <TITLE>downtimeMon Dashboard (v" + _dtMonVer + ")</TITLE>"
    ret += "    </HEAD>"        
    ret += "    <BODY>"   
    ret += "        <TABLE><TBODY>"
    ret += prep_response_Dashboard_RecentContent(downtimeData, executionData)     
    ret += prep_response_Dashboard_downtimeContent(downtimeData)     
    ret += prep_response_Dashboard_executionContent(executionData)     
    ret += "        </TBODY></TABLE>"
    ret += "    </BODY>"        
    ret += "</HTML>"

    return ret


def prep_response_Dashboard_RecentContent(downtimeData, executionData):
    dtData = None
    if downtimeData != None and len(downtimeData) > 0:
        dtData = DowntimeEntryObject.fromDowntimeEntryData(str(downtimeData[-1]))
    
    eData = None
    if executionData != None and len(executionData) > 0:
        eData = executionData[-1]

    ret = ""
    ret += "<TR><TD style='width:100%'>"
    ret += "    <TABLE style='width:100%'><TBODY>"
    ret += "    <TR><TD colspan=100 style='background:black;font-size:2rem; color:#e0e0e0; padding:10px; width:100%'><STRONG>downtimeMon Dashboard</STRONG></FONT>&nbsp;<FONT style='font-size:.85rem'>(v" + _dtMonVer + ")</FONT></TD></TR>"
    ret += "    <TR><TD colspan=100 style='font-size:1.75rem'><STRONG>Recent Data</STRONG></FONT></TD></TR>"
    if eData == None:
        ret += "    <TR><TD colspan=100><FONT style='font-size:1.1rem'><STRONG>Last Execution:</STRONG></FONT> &nbsp;&nbsp;&nbsp;No execution data exists</TD></TR>"
    else:
        ret += "    <TR><TD colspan=100><FONT style='font-size:1.1rem'><STRONG>Last Execution:</STRONG></FONT> &nbsp;&nbsp;&nbsp;" + eData + "</TD></TR>"
    ret += "    <TR><TD colspan=100 style='font-size:1.1rem'><STRONG>Last Downtime</STRONG></TD></TR>"
    if dtData == None:
        ret += "    <TR><TD style='padding-left:10px'>No downtime data exists</TD></TR>"
    else:
        ret += "    <TR><TD style='padding-left:10px'>" + dtData.toUiPanel(False) + "</TD></TR>"
    ret += "    </TBODY></TABLE>"
    ret += "</TD></TR>"
    return ret


def prep_response_Dashboard_downtimeContent(downtimeData):
    # Read downtimeLogFile
    # Display in decending order
    ret = ""
    ret += "<TR><TD colspan=100 style='font-size:1.75rem; padding-top:15px'><STRONG>Downtime Data</STRONG> (descending)</TD></TR>"
    ret += "<TR><TD colspan=100 style='font-size:1.25rem'>File: " + _downtimeLogFile + "</TD></TR>"
    for oneOutage in reversed(downtimeData):
        ret += "<TR><TD colspan=100 style='font-size:1.0rem; padding-left:15px'>" + DowntimeEntryObject.fromDowntimeEntryData(str(oneOutage)).toUiPanel(True) + "</TD></TR>"
    return ret


def prep_response_Dashboard_executionContent(executionData):
    # Read executionLogFile
    # Display in descending order
    ret = ""
    ret += "<TR><TD colspan=100 style='font-size:1.75rem; padding-top:20px'><STRONG>Execution Data</STRONG> (descending)</TD></TR>"
    ret += "<TR><TD colspan=100 style='font-size:1.25rem'>File: " + _executionLogFile + "</TD></TR>"
    for oneExec in reversed(executionData):
        ret += "<TR><TD colspan=100 style='font-size:1.0rem; padding-left:15px'>" + oneExec + "</TD></TR>"
    return ret


def load_downtimeFileContent():
    if not os.path.exists(_downtimeLogFile):
        return []
    else:
        lines = []
        with open(_downtimeLogFile, 'r') as f:
            for line in f:
                lines.append(line.strip())
        return lines


def load_executionFileContent():
    if not os.path.exists(_executionLogFile):
        return []
    else:
        lines = []
        with open(_executionLogFile, 'r') as f:
            for line in f:
                lines.append(line.strip())
        return lines


class DowntimeEntryObject:
    def __init__(self, outageStart, outageEnd, outageMins, testInterval):
        self.outageStart = outageStart
        self.outageEnd = outageEnd
        self.outageMins = outageMins
        self.testInterval = testInterval

    # Static factory method
    def fromDowntimeEntryData(dteData):
        try:
            jsonData = json.loads(dteData)
            dtStart = jsonData["lastExecutionFileEntry"]
            dtEnd = jsonData["currentTimestamp"]
            dtMins = jsonData["down_minutes"]
            dtInterval = jsonData["test_interval_secs"]
        except Exception as e:
            dtStart = 'Error: ' + str(e)
            dtEnd = None
            dtMins = None
            dtInterval = None
        return DowntimeEntryObject(dtStart, dtEnd, dtMins, dtInterval)

    # Instance 
    def toUiPanel(self, withBorder):
        ret = ""
        ret += "<TABLE style='border-collapse:collapse;'><TBODY>"
        if withBorder:
            ret += "  <TR style='border-top: 1px solid black;'>"
        else:
            ret += "  <TR>"
        ret += "    <TD><i>Start:</i></TD>"
        ret += "    <TD style='padding-left:5px'>" + str(self.outageStart) + "</TD>"
        ret += "    <TD style='padding-left:10px'>&nbsp;</TD>"
        ret += "    <TD style='padding-left:5px'><i>Test Interval (secs):</i></TD>"
        ret += "    <TD style='padding-left:5px'>" + str(self.testInterval) + "</TD>"
        ret += "  </TR>"
        # if withBorder:
        #     ret += "  <TR style='border-bottom: 1px solid black;'>"
        # else:
        ret += "  <TR>"
        ret += "    <TD style='padding-left:5px; padding-bottom:10px;'><i>End:</i></TD>"
        ret += "    <TD style='padding-left:5px; padding-bottom:10px;'>" + str(self.outageEnd) + "</TD>"
        ret += "    <TD style='padding-left:10px; padding-bottom:10px;'>&nbsp;</TD>"
        ret += "    <TD style='padding-left:5px; padding-bottom:10px;'><STRONG><i>Down (mins):</i></STRONG></TD>"
        ret += "    <TD style='padding-left:5px; padding-bottom:10px;'><STRONG>" + str(self.outageMins) + "</STRONG></TD>"
        ret += "  </TR>"
        ret += "</TBODY></TABLE>"
        return ret


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            print(f"GET Generating 200 Response")
            self.send_response(200)
            self.end_headers()
            content = prep_response_Dashboard()
            self.wfile.write(str(content).encode('utf-8'))
            print(f"GET 200 Response | Complete")
        else:
            print(f"GET Generating 404 Response")
            self.send_response(404)
            self.end_headers()
            self.wfile.write("".encode('utf-8'))
            print(f"GET 404 Response | Complete")

    def do_POST(self):
        print(f"POST Response Here")
        # Handle POST requests
        pass

Handler = MyHTTPRequestHandler

socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", _serverPort), Handler) as httpd:
    print("Serving downtimeMon on port", _serverPort)
    httpd.serve_forever()


