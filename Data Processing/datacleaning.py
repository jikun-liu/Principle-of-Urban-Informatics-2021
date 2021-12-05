import pandas as pd
import os

os.chdir('../data')
df = pd.read_csv('DSNY_Monthly_Tonnage_Data.csv')
df = df[['BOROUGH','MONTH','REFUSETONSCOLLECTED','PAPERTONSCOLLECTED','MGPTONSCOLLECTED']]
df['MONTH'] = pd.to_datetime(df['MONTH'])
df['year'] = df['MONTH'].dt.year
df['month'] = df['MONTH'].dt.month
df.rename(columns={'BOROUGH':'Borough','REFUSETONSCOLLECTED':'Refuse',
                   'PAPERTONSCOLLECTED':'Paper','MGPTONSCOLLECTED':'MGP'},
                   inplace = True)
df = df[['Borough','year','month','Refuse','Paper','MGP']]
df = df.loc[df['year']>=2020]
df.dropna(inplace=True)
df.replace('Staten Island', 'Staten',inplace=True)
path = os.getcwd()+'\\tonnage.csv'
df.to_csv(path,index=False)
