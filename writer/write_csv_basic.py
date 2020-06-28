import sys

try:
  counties = sys.argv[1].split(',')
  candidate = sys.argv[2]
  counts = sys.argv[3].split(',')
except IndexError:
  print('Not enough arguments. Did you use three?')
  sys.exit()

if len(counties) == len(counts):
  for index, count in enumerate(counts):
    line = f'{counties[index]},President,,Democrat,{candidate},{count}\n'

    with open('csv/csv.csv', 'a') as f:
      f.write(line)
else:
  raise Exception('mismatch in length of counties and vote counts')