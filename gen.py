import requests
import sys
import os
import pickle
from bs4 import BeautifulSoup

settings = {
    "PROBLEM_ID": None,
    "single case": True,
    "case cnt": 1,
}

CONTEST_ID = sys.argv[1] # contest id (not contest number)
PROBLEM_ID = sys.argv[2].capitalize() # problem letter (TODO: make it optional)

if len(sys.argv) == 4:
    TEMPLATE_PATH = sys.argv[3]
    os.system(f"cat {TEMPLATE_PATH} > {PROBLEM_ID}.cpp")

PATH = os.getcwd()

url = "https://www.codeforces.com/contest/" + CONTEST_ID + "/problem/" + PROBLEM_ID
req = requests.get(url)
if not req.ok:
    print("Could not find the problem page!")
    sys.exit(-1)

soup = BeautifulSoup(req.content, 'html.parser')
case_div = soup.find("div", {"class": "sample-test"})

input_div = case_div.find_all("div", {"class": "input"})
case_cnt = len(input_div)
single_case = True

if case_cnt > 1:
    single_case = False

in_file = open(f"{PATH}/{PROBLEM_ID}.in", "w")

for input in input_div:
    input = input.pre

    final = ""
    for element in input:
        inp = element.text

        if case_cnt == 1:
            in_file.write(inp.strip() + "\n")
        else:
            inp = inp.replace("\n", " ").strip()
            final += inp + " "

    if case_cnt > 1:
        in_file.write(final + "\n")

in_file.close()

output_div = case_div.find_all("div", {"class": "output"})

out_file = open(f"{PATH}/{PROBLEM_ID}.out", "w")
for out in output_div:
    out = out.pre
    for br in out.find_all("br"):
        br.replace_with("\n")

    res = out.text
    if case_cnt > 1:
        res = res.replace("\n", " ")

    out_file.write(res + "\n")

settings["PROBLEM_ID"] = PROBLEM_ID
settings["case cnt"] = case_cnt
settings["single case"] = single_case

f = open(f"{PATH}/config.cfg", "wb")
pickle.dump(settings, f)
f.close()
