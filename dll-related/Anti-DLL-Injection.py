import time
import ctypes
from ctypes import wintypes, windll

# This script was tested on Win10 Pro/Win 11 Pro using process hacker dll injection. Probably blocks the other methods too...

# define the constants
ProcessSignaturePolicyMitigation = 8

# define the PROCESS_MITIGATION_BINARY_SIGNATURE_POLICY structure
class PROCESS_MITIGATION_BINARY_SIGNATURE_POLICY(ctypes.Structure):
    _fields_ = [("MicrosoftSignedOnly", wintypes.DWORD)]

# load the kernelbase.dll and the SetProcessMitigationPolicy function from windll (i love ctypes)
kernelbase = windll.kernelbase
SetProcessMitigationPolicy = kernelbase.SetProcessMitigationPolicy

def set_process_mitigation_policy(policy, lpBuffer, size): # define the main script
    success = SetProcessMitigationPolicy(policy, ctypes.byref(lpBuffer), size)
    if success != 0:
        return True, None
    else:
        error_code = ctypes.GetLastError()
        if error_code != 0:
            return False, ctypes.WinError(error_code)
        return False, None

def configure_process_mitigation_policy(): # define/load the policy config
    OnlyMicrosoftBinaries = PROCESS_MITIGATION_BINARY_SIGNATURE_POLICY()
    OnlyMicrosoftBinaries.MicrosoftSignedOnly = 1

    success, err = set_process_mitigation_policy(ProcessSignaturePolicyMitigation,
                                                 OnlyMicrosoftBinaries,
                                                 ctypes.sizeof(OnlyMicrosoftBinaries))
    if err:
        print("Failed:", err)
    elif success:
        print("Success!")
    else:
        print("Failed!")

configure_process_mitigation_policy()


# Your code below here...
