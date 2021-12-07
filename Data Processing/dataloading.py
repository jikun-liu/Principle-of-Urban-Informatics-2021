import pandas as pd
import os

# only include file specified in list; merge at request
def dataloader(file_list, merge=False):
    os.chdir('../data')
    out_df = pd.DataFrame({'Borough': []})
    df_dict = {}

    for name in file_list:
        if name == "scorecard":
            if merge == False:
                df_dict[name] = pd.read_csv('scorecard-inspection.CSV')
            else:
                if len(out_df.index) == 0:
                    out_df = pd.read_csv('scorecard-inspection.CSV')
                else:
                    df = pd.read_csv('scorecard-inspection.CSV')
                    out_df = out_df.merge(df, on='Borough')

        elif name == "tonnage":
            if merge == False:
                df_dict[name] = pd.read_csv('tonnage.csv')
            else:
                if len(out_df.index) == 0:
                    out_df = pd.read_csv('tonnage.csv')
                else:
                    df = pd.read_csv('tonnage.csv')
                    out_df = out_df.merge(df, on='Borough')

        elif name == "covid":
            if merge == False:
                df_dict[name] = pd.read_csv('covid-nyc.csv')
            else:
                if len(out_df.index) == 0:
                    out_df = pd.read_csv('covid-nyc.csv')
                else:
                    df = pd.read_csv('covid-nyc.csv')
                    out_df = out_df.merge(df, on='Borough')

    if merge == False:
        return df_dict

    return out_df

print(dataloader(["scorecard",'tonnage','covid']))
