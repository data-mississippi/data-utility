import sys
from csv import reader
import pandas as pd
import time

def get_counties_list():
  counties = []

  with open(counties_path, 'r') as f:
    csv_reader = reader(f)
    
    # there should only be one row
    for row in csv_reader:
      counties = row

  print(f'Processing results for these counties: {counties}')
  return counties


def write_candidate_csv_lines(row):
  candidate = row.pop(0)

  if len(counties) == len(row):
    lines = []
    csv_string = ''

    print('\n') # for the CLI display...

    for index, votes in enumerate(row):
      line = f'{counties[index]},{office},{district},{party},{candidate},{votes}\n'
      print(line)
      csv_string += line

    # pause execution to check work
    key_input = input('\nVerify the results are correct and press enter to continue. Press ctrl + c to quit.\n')

    # finally, write the rows to the csv file
    with open(temp_file, 'a') as f:
      f.write(csv_string)
  else:
    print('Invalid inputs. There is likely a mismatch in how many counties are input and how many vote tallies were input for a candidate.')
    sys.exit()


def build_csv():
  # get the candidates and their votes
  with open(candidate_votes_path, 'r') as f:
    csv_reader = reader(f)

    # each row is a candidate's results
    # and there can be multiple candidates,
    # so loop through each row to write 
    # the results for each candidate
    for results in csv_reader:
      write_candidate_csv_lines(results)


def sort_csv(temp_file):
  df = pd.read_csv(temp_file, header=None)
  df.columns = ['county', 'office', 'district', 'party', 'candidate', 'votes']
  df.drop_duplicates(subset=None, inplace=True)
  df.sort_values(by=['candidate', 'county'], inplace=True)
  df.to_csv('sorted_results.csv', index=False)


if __name__ == '__main__':
  try:
    counties_path = sys.argv[1]
    candidate_votes_path = sys.argv[2]
    office = sys.argv[3]
    district = sys.argv[4]
    party = sys.argv[5]
    
  except IndexError:
    print('Not enough arguments. Please enter your source file locations.')
    sys.exit()

  counties = get_counties_list()
  timestamp = time.strftime("%Y%m%d-%H%M%S")
  temp_file = f'tmp/results-{timestamp}.csv'
  build_csv()
  sort_csv(temp_file)