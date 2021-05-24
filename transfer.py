import os
import time
from xml.dom.minidom import parse
import xml.dom.minidom
import importlib
sn = ""
result = {"bank":"CCB","deviceid":"8HT4DEQODUAQNFMJ","password":"861690"}


bank = result['bank']
module = importlib.import_module(bank+"."+bank)
adb_obj_class = getattr(module,bank)
bank_class = adb_obj_class(result)
tresult = bank_class.transfer()
if tresult == "101":
    print("no device found")
    

        
        



