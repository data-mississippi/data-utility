# data-utility
This contains a data entry CLI for MS statewide election results. It's for a very specific workflow and probably useless to other people, except as an example on how to do this.

Your system requires Python 3.7. Setup your virtual environment like this:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Then run the script, with the arguments (explained below):
```
cd writer
python write_csv.py counties.csv candidate_votes.csv President '' Democrat
```

## Here is how it works:
  This script is used with Tabula. 
  1. Export a page of results from the PDF with Tabula
  2. Take the results from the PDF and create a file called `candidate_votes.csv`. Put each candidate's name and results in that file -- separated by commas and with each candidate on a new line. 
  3. Write the associated county names on one line in a file called `counties.csv`. Also separated by commas. 
  
  **The order of votes in `candidate_votes.csv` must map to the list of `counties.csv`. If this mapping is wrong, then the output file will be wrong.**

For instance:
```
# candidate_votes.csv

Elizabeth Warren,24,160,37,59
```

```
# counties.csv

Iuka,Lee,Pontotoc,Union
```

This would mean Iuka = 24, Lee = 160, Pontotoc = 37, and Union = 59. If your output is wrong, then it's probably mapped incorrectly.

## CLI Arguments
There are demo files which already exist in the repo. In your virtual environment, execute the script:
```
python write_csv.py counties.csv candidate_votes.csv President '' Democrat
```

The CLI takes five arguments: 
  1) the path of your `candidate_votes.csv`
  2) the path of your `counties.csv`
  3) office seat 
  4) district (empty string if none)
  5) party

## etc
The script pauses periodically, so that you can check your work against the certified election results. Once you've verified that, the script continues. If there's something wrong with the output, then it's most likely that the input csv file mapping is mismatched.

When the script is done, it writes the results into a new csv file called `sorted_results.csv`. The results are grouped by candidates and sorted alphabetically by county. This file will be rewritten every time the script runs, so before you run the script again, rename the `sorted_results.csv` file or save the results elsewhere.

Currently, the preprocessed results are dumped in the `/tmp` folder. Might want to clear that out or submit a PR with a better solution.

Originally, this was like a 20 line script but now I've probably spent too much time and made this more complicated than the first iteration...if you want to use that script, it's called `write_csv_basic.py`. 