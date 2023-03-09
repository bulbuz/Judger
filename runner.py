import os
import sys
import pickle
import subprocess
import time

PATH = os.getcwd()

# load in the settings
f = open(f"{PATH}/config.cfg", "rb")
settings = pickle.load(f)
f.close()

# colors
ACCEPTED = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
NORMAL = '\33[0m'

PROBLEM_ID = settings["PROBLEM_ID"]

out_file = open(f"{PATH}/{PROBLEM_ID}.out", "r")
ans = []
for line in out_file:
    s = line.strip().replace('\n', "")
    if s != "":
        ans.append(s)
out_file.close()

print(f"[DEBUG] Compiling {PROBLEM_ID}.cpp")
os.system(f"g++ {PATH}/{PROBLEM_ID}.cpp -std=c++17 -o {PATH}/{PROBLEM_ID}")
result = []
delta = 0

case_cnt = settings["case cnt"]

if settings["single case"]:
    start = time.perf_counter()
    out = subprocess.check_output(f"{PATH}/{PROBLEM_ID} < {PATH}/{PROBLEM_ID}.in", shell=True, universal_newlines=True)
    delta = time.perf_counter() - start
    result = out.splitlines()
else:
    inp = []
    in_file = open(f"{PATH}/{PROBLEM_ID}.in", "r")

    for line in in_file:
        inp.append(line)

    for i in range(case_cnt):
        start = time.perf_counter()
        out = subprocess.run([f"{PATH}/{PROBLEM_ID}"], stdout=subprocess.PIPE, text=True, input=inp[i])
        temp_delta = time.perf_counter() - start

        delta += temp_delta
        out = out.stdout.strip("\n")
        result.append(out)

passed_tests = 0
accepted = True

if len(ans) != len(result):
    print(WARNING + "[WARNING] Unexpected output length!")
    accepted = False
    missmatches = [i + 1 for i in range(case_cnt)]
    print(NORMAL, end="")
else:
    missmatches = []
    for i in range(len(ans)):
        if result[i] != ans[i]:
            missmatches.append(i + 1)
            accepted = False
        else:
            passed_tests += 1

    if settings["single case"]:
        if passed_tests != len(ans):
            passed_tests = 0
        else:
            passed_tests = 1

# output
print(f"Time: {delta:.2f} ms")
print("---------------")
print("Output:")
for line in result:
    print(line)
print("---------------")

print("Expected:")
for line in ans:
    print(line)
print("---------------")

if accepted:
    print(ACCEPTED + "Passed!\n")
else:
    print("Missmatch at ", end="")
    for i in range(len(missmatches) - 1):
        print(str(missmatches[i]) + ", ", end="")

    print(missmatches[-1])

    print(FAIL + "\nFailed!\n")

print(f" {passed_tests} / {case_cnt}\n")
