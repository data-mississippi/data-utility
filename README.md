# data-utility
This contains a data entry CLI for MS statewide election results. It's for a very specific workflow and probably useless to other people, except as an example on how to do this. Originally, this was like a 20 line script but now I've probably spent too much time and made this more complicated than the first iteration...if you want to use that script, it's called `elections.py`. Your system requires Python 3.7.

It's used with Tabula, which extracts the data from the PDF. Export a page of results from the PDF with Tabula, put those in two files (explained below), and then run the script. 

Here is how it works:
  1) take the results from the PDF and create a file called `candidate_counts.csv`. Put each candidate's name + results on a newline in that file. Write the associated county names in a file called `counties.csv`.

For instance:
```
# candidate_counts.csv

Bernie Sanders,24,16,37
```

```
# counties.csv

Adams,Attalla,Amite
```

The CLI takes five arguments: 
  1) the path of your candidate_counts.csv
  2) the path of your counties.csv 
  3) office seat 
  4) district (empty string if none)
  5) party

There are demo files which already exist in the repo. In your terminal execute the script:
`python3 write_csv.py counties.csv candidate_counts.csv President '' Democrat`

Since this is data entry, I want to be sure that I'm inputting the correct values. To do that, the script pauses after each candidate's results are parsed, so that you can check your work against the certified election results. Once you've verified that, the script continues. If there's something wrong with the output, then it's most likely that the input csv files are mismatched.

When the script is done, it writes the results into a new csv file. The results are grouped by candidates and within each grouping, sorted alphabetically by county. This file will be rewritten every time the script runs, so save the results elsewhere.