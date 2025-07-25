import json
import os
import shutil
import subprocess

def libExists():
    return True

def dir_create(dirPath):
    if not os.path.exists(dirPath):
        try:
            os.mkdir(dirPath)
            print(f"Directory '{dirPath}' created successfully.")
        except FileExistsError:
            print(f"Directory '{dirPath}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create directory '{dirPath}'.")
            return False
        except Exception as e:
            print(f"An error occurred creating directory '{dirPath}': \n{e}")
            return False
    return True


def file_copy(src, dst):
    try:
        shutil.copy2(src, dst)
        print(f"'{src}' successfully copied to '{dst}'")
    except PermissionError:
        print(f"Permission denied: Unable to copy '{src}' to '{dst}'.")
        return False
    except Exception as e:
        print(f"An error occurred copying '{src}' to '{dst}': \n{e}")
        return False
    return True


def objectExists(objTitle, obj):
    if obj == None:
        return False
    return True

def objectPopulated_String(objTitle, obj):
    if obj == None:
        return False
    if len(str(obj)) == 0:
        return False
    return True

def objectPopulated_Int(objTitle, obj):
    if obj == None:
        return False
    if isinstance(obj, int):
        return True
    else:
        return False


def service_defs_reload():
    subprocess.run(["sudo", "systemctl", "daemon-reload"]) 

def service_enable(svcName):
    subprocess.run(["sudo", "systemctl", "enable", svcName]) 

def service_start(svcName):
    subprocess.run(["sudo", "systemctl", "start", svcName]) 

def service_stop(svcName):
    subprocess.run(["sudo", "systemctl", "stop", svcName]) 

def service_status(svcName):
    result = subprocess.run(
        ["sudo", "systemctl", "status", svcName],
        capture_output = True,  # Python >= 3.7 only
        text = True             # Python >= 3.7 only
    )
    return str(result) 


class PsPythonSettingsFile:
    def __init__(self, settingsFile):
        self._jsonObj = None
        with open(settingsFile, 'r') as jsonFile:
            self._jsonObj = json.load(jsonFile)        

    def setting_Get(self, settingName):
        retVal = None
        if self._jsonObj != None:
            try:
                setObj = self._jsonObj["settings"]
                if setObj != None:
                    try:
                        setObj = setObj[settingName]
                        if setObj != None:
                            retVal = str(setObj)
                    except:
                        #Do nothing
                        retVal = None
            except:
                #Do nothing
                retVal = None
        return retVal

