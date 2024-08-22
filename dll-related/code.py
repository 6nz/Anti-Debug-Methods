# THIS WHOLE CODE IS TO SHOW HOW TO DETECT SRC MODIFICATION AT "REAL-TIME"

import time

def newprog():
    print("XD")

try:
    oldprog = newprog
except Exception as e:
    print(f"Fail: {e}")

print("\nDONE!\n")
time.sleep(1)
