import requests
import sys
import pickle
from bs4 import BeautifulSoup

settings = {
    "PROBLEM_ID": None,
    "single case": True,
    "case cnt": 1,
}

CONTEST_ID = sys.argv[1] # contest id (not contest number)
PROBLEM_ID = sys.argv[2].capitalize() # problem letter (TODO: make it optional)

url = "https://www.codeforces.com/contest/" + CONTEST_ID + "/problem/" + PROBLEM_ID
req = requests.get(url)
if not req.ok:
    print("Could not find the problem page!")
    sys.exit()

soup = BeautifulSoup(req.content, 'html.parser')
input_div = soup.find_all("div", {"class": "input"})

single_case = True
case_cnt = 0

in_file = open(f"{PROBLEM_ID}.in", "w")
for input in input_div:
    input = input.pre

    for test_case in input:
        if test_case.text != "\n" and test_case.text != "":
            in_file.write(test_case.text + "\n")

        # check for separate test cases
        if len(input_div) > 1:
            single_case = False
            case_cnt += 1

in_file.close()

out_file = open(f"{PROBLEM_ID}.out", "w")
output_div = soup.find_all("div", {"class": "output"})

for output in output_div:
    output = output.pre
    for test_case in output:
        out_file.write(test_case.text)

out_file.close()

settings["PROBLEM_ID"] = PROBLEM_ID
settings["case cnt"] = case_cnt
settings["single case"] = single_case

f = open("config.cfg", "wb")
pickle.dump(settings, f)
f.close()
