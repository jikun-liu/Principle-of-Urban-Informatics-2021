import os
import sys
import pandas as pd
import scipy
import numpy as np

from dataloading import dataloader

Boroughs = ['Manhattan','Queens','Brooklyn','Bronx','Staten']
df_dict = dataloader(['restaurant','covid','tonnage','water','indoor'])
df_rest = df_dict['restaurant']
df_ton = df_dict['tonnage']
df_covid = df_dict['covid']
df_water = df_dict['water']
df_indoor = df_dict['indoor']
new_case_by_month = df_covid[['year','month','Borough','New Positives']].groupby(by=['year','month','Borough']).sum()

print('Restaurant grade:')
# get restaurant correlation coefficients
for boro in Boroughs:
    df_man = df_rest.loc[df_rest['Borough']==boro]
    target_month = [7,8,9,10,11,12]
    target_year = 2021
    dfs = df_man.groupby(by=['year','month'])
    grades = pd.DataFrame()
    for m in target_month:
        curr_df = dfs.get_group((target_year,m))[['grade','month']]
        curr_df.rename(columns={'month':'m'+str(m)}, inplace = True)
        curr_df = curr_df.groupby('grade').count()
        grades = pd.concat([grades,curr_df],axis=1)
    grades = grades.fillna(0)
    covid_counts = []
    for m in target_month:
        covid_counts.append(new_case_by_month.loc[target_year,m,boro]['New Positives'])
    print('For borough',boro+':')
    coef_mat = np.corrcoef(grades,covid_counts)
    print(coef_mat[:,coef_mat.shape[0]-1])

def coef_by_borough(dataframe, title, list_var, method):
    print(title)
    # chopped of 2020.1~2 to fit covid data
    df = dataframe
    df = df.loc[(df['year']>=2021) | (df['year']==2020) & (df['month']>=3)]

    for boro in Boroughs:
        df_man = df.loc[df['Borough']==boro]
        dfs = df_man.groupby(by=['year','month']).aggregate(method)
        agg = pd.DataFrame()
        for ym in dfs.index.unique():
            curr_df = dfs.loc[ym[0],ym[1]][list_var]
            agg = pd.concat([agg,curr_df],axis=1)
        agg.fillna(0,inplace=True)
        covid_counts = []
        for ym in dfs.index.unique():
            covid_counts.append(new_case_by_month.loc[ym[0],ym[1],boro]['New Positives'])

        print('For borough',boro+':')
        coef_mat = np.corrcoef(agg,covid_counts)
        print(coef_mat[:,coef_mat.shape[0]-1])


coef_by_borough(df_ton,'\nTonnage:',['Refuse','Paper','MGP'],'sum')
coef_by_borough(df_water,'\nWater:',['total cost'],'sum')
coef_by_borough(df_indoor,'\nIndoor complaints:',['zip'],'count')
