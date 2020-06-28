# csv writer
This contains a data entry CLI for MS statewide election results. It's for a very specific workflow and probably useless to other people, except as an example on how to do this.

Your system requires Python 3.7. Set up your virtual environment like this:
```
cd csv_writer
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Then run the script, with the arguments (explained below):
```
python write_csv.py source/jurisdictions.csv source/candidate_votes.csv Senate Democrat County 1
```

## Here is how it works:
  This script is used with Tabula. 
  1. Export a page of results from the PDF with Tabula
  2. Take the results from the PDF and create a file called `candidate_votes.csv`. Put each candidate's name and vote results in that file. This data must be separated by commas and with each candidate on a new line. 
  3. Write the associated jurisdiction names (counties or precints) on one line in a file called `jurisdictions.csv`. Also separated by commas. 
  
  **The order of votes in `candidate_votes.csv` must map to the list of `jurisdictions.csv`. If this mapping is wrong, then the output file will be wrong.**

For instance:
```
# candidate_votes.csv

Elizabeth Warren,24,160,37,59
```

```
# jurisdictions.csv

Itawamba,Lee,Pontotoc,Union
```

This would mean Itawamba = 24, Lee = 160, Pontotoc = 37, and Union = 59. If your output is wrong, then this mapping is wrong.

## CLI Arguments
There are demo files which already exist in the repo. In your virtual environment, execute the script:
```
python write_csv.py source/jurisdictions.csv source/candidate_votes.csv President Democrat County
```

The CLI takes 6 arguments: 
  1) the path of your `candidate_votes.csv` (required)
  2) the path of your `jurisdictions.csv` (required)
  3) office seat (required)
  4) party (required)
  5) jurisdiction (required)
  6) district (optional)

## etc
The script pauses periodically, so that you can check your work against the certified election results. Once you've verified that, the script continues. If there's something wrong with the output, then it's most likely that the input csv files have mismatched mapping.

When the script is done, it writes the results into a new csv file called `results-{timestamp}.csv`. The results are grouped by candidates and sorted alphabetically by county. When I do this, I go through the election results PDF and input the results page by page. That means I execute the script multiple times for an election. If you do it like that, then you'll need to combine all of these output files at the end. There is a helper script that does that called `combine_csv_output.py`. It creates a file called `final-sorted-output.csv`.

Originally, this was like a 20 line script but now I've probably spent too much time and made this more complicated than the first iteration...if you want to use that script, it's called `write_csv_basic.py`. 