import pandas as pd
import os

# only include file specified in list
def dataloader(file_list):
    os.chdir('../data')
    out_df = pd.DataFrame({'Borough': []})

    for name in file_list:
        if name == "scorecard":
            if len(out_df.index) == 0:
                out_df = pd.read_csv('scorecard-inspection.CSV')
            else:
                df = pd.read_csv('scorecard-inspection.CSV')
                out_df = out_df.merge(df, on='Borough')
        elif name == "tonnage":
            if len(out_df.index) == 0:
                out_df = pd.read_csv('tonnage.csv')
            else:
                df = pd.read_csv('tonnage.csv')
                out_df = out_df.merge(df, on='Borough')
    return out_df

print(dataloader(["scorecard",'tonnage']))
