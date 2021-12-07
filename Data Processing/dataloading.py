import pandas as pd
import os

# only include file specified in list; merge on column Borough at request
# Please do not merge unless YOU ARE ABSOLUTELY CONFIDENT
# Use Example:
# df_dict = dataloader(['covid','indoor','chir'])
# df_covid = df_dict['covid']
def dataloader(file_list, merge=False):
    cwd = os.getcwd()
    os.chdir('../data')
    df_dict = {}

    for name in file_list:
        if name == "scorecard":
            df_dict[name] = pd.read_csv('scorecard-inspection.CSV')
        elif name == "tonnage":
            df_dict[name] = pd.read_csv('tonnage.csv')
        elif name == "covid":
            df_dict[name] = pd.read_csv('covid-nyc.csv')
        elif name == "indoor":
            df_dict[name] = pd.read_csv('indoor-complaints.csv')
        elif name == "water":
            df_dict[name] = pd.read_csv('water-consumption.csv')
        elif name == "chir":
            df_dict[name] = pd.read_csv('chir.csv')
        elif name == "restaurant":
            df_dict[name] = pd.read_csv('restaurant-grade.csv')

    os.chdir(cwd)
    
    if merge == False:
        return df_dict
    out_df = pd.DataFrame()
    for key,val in df_dict.items():
        if len(out_df.index) == 0:
            out_df = val
        else:
            out_df = out_df.merge(val, on='Borough')
    return out_df
