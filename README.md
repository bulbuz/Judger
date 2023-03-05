# Judger
Automatically grades your codeforces solution against the sample test cases

---

## Use

Run **gen_test.py** with the command-line arguments:
- Contest id (**NOT** round number)
- Problem id (usually the letter)

It is necessary to run gen_test.py BEFORE runner.py since it fetches the samples.

Then run the **runner.py** to grade your solution.

**NOTE:** it is required to name your solution to the *capitalized* problem id

