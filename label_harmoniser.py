import os
import re
import pandas as pd

with open('./label1.txt') as f:
    raw = f.readlines()[4:]

pattern = r'(\w*)/(\w*)/(\d{4})_(\d{2})_(\d{2})_(\d{2})_(\d{2})_(\d{2})(\w*\.avi)\s(\d*)\s(\d*)\s(\d*)'

columns = ['file_id', 'quality', 'crowd',
           'year', 'month', 'day', 'hour', 'min', 'sec',
           'video_id', 'EnteringNumber', 'ExitingNumber', 'VideoType']

df = pd.DataFrame(columns=columns)

c = 0
for line in raw:
    c += 1
    result = re.search(pattern, line)
    if result:
        temp = pd.DataFrame(columns=columns, data=[
                            ['file_id']+list(result.groups())])

        df = pd.concat([df, temp], axis=0)
    else:
        print("error in line", c)

print(df.head())
