import threading
import time
import inspect

def oldprog():
    print("OLDPROG FUNCTION ALIVE...")

def func_prot():
    while True:
        time.sleep(0.1) # can be adjusted
        oldprog()
        try:
            inspect.getsource(oldprog) # If the attacker modifies the source code by injecting the code.py to the running process ---> this will detect if the "oldprog" function changes
            print("Checked...")
        except Exception as E:
            print("Possible cracking/bypassing detected.")
            print(f"ELog: {E}")
            time.sleep(3)
            os._exit(1)


threading.Thread(target=func_prot).start() # you can also use multiprocessing for this or anything you want
time.sleep(1)
