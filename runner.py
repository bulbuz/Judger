import os
import sys
import pickle
import subprocess
import time

# load in the settings
f = open("config.cfg", "rb")
settings = pickle.load(f)
f.close()

# colors
ACCEPTED = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'

PROBLEM_ID = settings["PROBLEM_ID"]

out_file = open(f"{PROBLEM_ID}.out", "r")
dat = []
for line in out_file:
    s = line.replace('\n', "")
    if s != "":
        dat.append(s)
out_file.close()

print(f"[DEBUG] Compiling {PROBLEM_ID}.cpp")
os.system(f"g++ {PROBLEM_ID}.cpp -std=c++17 -o {PROBLEM_ID}")

# single test case
if settings["single case"]:

    start = time.perf_counter()
    res = subprocess.check_output(f"./{PROBLEM_ID} < {PROBLEM_ID}.in", shell=True, universal_newlines=True)
    delta = (time.perf_counter() - start)
    res = res.splitlines()

    print(f"Time: {delta:.2f} ms")
    print("---------------")
    print("Output:")
    for line in res:
        print(line)
    print("---------------")

    print("Expected:")

    for out in dat:
        print(out)

    print("---------------")

    if len(dat) != len(res):
        print(WARNING + "[WARNING] Unexpected output length!")
        print("Aborted")
        sys.exit()

    ok_tests = 0
    accepted = True
    for i in range(len(dat)):
        if dat[i] != res[i]:
            accepted = False
            print(f"Expected {dat[i]}, got {res[i]}!")
        else:
            ok_tests += 1
            
    if accepted:
        print(ACCEPTED + "Passed!\n")
        print(f" {ok_tests} / {len(dat)}\n")
    else:
        print(FAIL + "Failed!")
else:
    test_cases = settings["case cnt"]

    inp = []
    in_file = open(f"{PROBLEM_ID}.in", "r")
    for line in in_file:
        s = line.replace('\n', '')
        if s != "":
            inp.append(s)
    in_file.close()

    start = time.perf_counter()

    ok_tests = 0
    accepted = True

    result = []
    for i in range(test_cases):
        res = subprocess.run([f"./{PROBLEM_ID}"], stdout=subprocess.PIPE, text=True, input=inp[i])
        res = res.stdout.strip('\n')

        if dat[i] != res:
            accepted = False
        else:
            ok_tests += 1
        
        result.append(res)

    delta = (time.perf_counter() - start)

    print(f"Time: {delta:.2f} ms")
    print("---------------")
    print("Output:")
    for line in result:
        print(line)
    print("---------------")

    print("Expected:")

    for out in dat:
        print(out)

    print("---------------")

    if accepted:
        print(ACCEPTED + "Passed!\n")
        print(f" {ok_tests} / {len(dat)}\n")
    else:
        print()
        for i in range(test_cases):
            if dat[i] != result[i]:
                print(f"Expected {dat[i]}, got {result[i]}!")

        print(FAIL + "\nFailed!\n")