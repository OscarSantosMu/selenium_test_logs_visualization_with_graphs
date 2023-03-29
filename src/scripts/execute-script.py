import os
import time

i = 0
while i < 100:
    try:
        os.system("generate-logs.py")
        print(f"{i}th iteration: Success")
    except Exception as e:
        print(f"{i}th iteration: Fail")
        print(f"Reason: {e}")
    i += 1
    time.sleep(30)
