import sys
import os
from csv import reader
import pandas as pd
import time
from io import StringIO
          

def main():
  arg_map = parse_arguments()

  # build the csv lines and store it in a string
  tmp_csv = build_tmp_csv(arg_map)

  # final csv output
  sort_and_output_final_csv(tmp_csv, arg_map)


def parse_arguments():
  arg_map = {}

  try:
    arg_map.update({
      'jurisdiction_list_path': sys.argv[1],
      'candidate_votes_path': sys.argv[2],
      'office': sys.argv[3],
      'party': sys.argv[4],
      'jurisdiction_level': sys.argv[5]
    })
    
  except IndexError:
    print('Not enough arguments. See README.md for list of required arguments.')
    sys.exit()

  try:
    district = sys.argv[6]
  except IndexError:
    district = ''

  arg_map.update({
    'jurisdiction_list': get_jurisdiction_list(arg_map.get('jurisdiction_list_path')),
    'district': district,
    'results_file_name': f'results-{time.strftime("%Y%m%d-%H%M%S")}.csv',
    'csv_header': [arg_map.get('jurisdiction_level').lower(), 'office', 'district', 'party', 'candidate', 'votes']
  })

  return arg_map


def get_jurisdiction_list(path):
  """Returns list of jurisdictions from the jurisdiction.csv"""
  jurisdiction = []

  with open(path, 'r') as f:
    csv_reader = reader(f)
    
    # there should only be one row
    jurisdictions = next(csv_reader)
    print(f'Processing results for these jurisdictions: {jurisdiction}')

  return jurisdictions


def build_tmp_csv(arg_map):
  """
    Builds a chunk of csv lines for each candidate.
    
    It opens the candidate_votes.csv file and loops through each line.
    Each line is a candidate's results and there can be multiple candidates in the csv. 
    Then it writes that candidate's csv lines to a temp_csv string.
  """
  temp_csv = ''

  with open(arg_map.get('candidate_votes_path'), 'r') as f:
    csv_reader = reader(f)

    for results in csv_reader:
      temp_csv += write_candidate_csv_lines(results, arg_map)
  
  return temp_csv


def write_candidate_csv_lines(row, arg_map):
  """
    Writes a candidate's csv lines to a csv_string.

    The program pauses once the candidate's lines have compiled,
    so the user can verify the output. Then it writes those lines to a temp file.
  """
  candidate = row.pop(0)
  jurisdiction_list = arg_map.get('jurisdiction_list')
  office = arg_map.get('office')
  district = arg_map.get('district', '')
  party = arg_map.get('party')
  csv_string = ''

  if len(jurisdiction_list) == len(row):
    lines = []

    print('\n') # for the CLI display...

    for index, votes in enumerate(row):
      line = f'{jurisdiction_list[index]},{office},{district},{party},{candidate},{votes}\n'
      print(line)
      csv_string += line

    # pause execution to check work
    key_input = input('\nVerify the results are correct and press enter to continue. Press ctrl + c to reject.\n')

    return csv_string

  else:
    print('Invalid inputs. There is likely a mismatch in how many jurisdictions are input and how many vote tallies were input for a candidate.')
    sys.exit()


def sort_and_output_final_csv(tmp_csv, arg_map):
  """
    Processes the tmp_csv for final output.
  """
  results_file = arg_map.get('results_file_name')
  csv_header = arg_map.get('csv_header')

  df = pd.read_csv(StringIO(tmp_csv), header=None)
  df.columns = csv_header
  df.drop_duplicates(subset=None, inplace=True)
  df.sort_values(by=['candidate', 'county'], inplace=True)
  df.to_csv(results_file, index=False)


if __name__ == '__main__':
  main()