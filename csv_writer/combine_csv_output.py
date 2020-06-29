import pandas as pd
import glob, os
 
df = pd.concat(map(pd.read_csv, glob.glob(os.path.join('', "results*.csv"))))
df.sort_values(by=['candidate', 'county'], inplace=True)
df.to_csv('sorted-house-output.csv', index=False)