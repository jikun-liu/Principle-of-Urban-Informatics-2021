import pandas as pd
import os

os.chdir('../data')
# df = pd.read_csv('1RAW-DSNY_Monthly_Tonnage_Data.csv')
# df = df[['BOROUGH','MONTH','REFUSETONSCOLLECTED','PAPERTONSCOLLECTED','MGPTONSCOLLECTED']]
# df['MONTH'] = pd.to_datetime(df['MONTH'])
# df['year'] = df['MONTH'].dt.year
# df['month'] = df['MONTH'].dt.month
# df.rename(columns={'BOROUGH':'Borough','REFUSETONSCOLLECTED':'Refuse',
#                    'PAPERTONSCOLLECTED':'Paper','MGPTONSCOLLECTED':'MGP'},
#                    inplace = True)
# df = df[['Borough','year','month','Refuse','Paper','MGP']]
# df = df.loc[df['year']>=2020]
# df.dropna(inplace=True)
# df.replace('Staten Island', 'Staten',inplace=True)
# path = os.getcwd()+'\\tonnage.csv'
# df.to_csv(path,index=False)

df = pd.read_csv('1RAW-New_York_State_Statewide_COVID-19_Testing.csv')
df = df[['Test Date','County','New Positives','Cumulative Number of Positives',
         'Total Number of Tests Performed',
         'Cumulative Number of Tests Performed']]
df = df.loc[df['County'].isin(['Kings','Queens','Bronx','New York','Richmond'])]
df['Test Date'] = pd.to_datetime(df['Test Date'])
df['year'] = df['Test Date'].dt.year
df['month'] = df['Test Date'].dt.month
df.rename(columns={'County':'Borough'}, inplace = True)
df.dropna(inplace=True)
df.replace(['Kings','Queens','Bronx','New York','Richmond'],
           ['Brooklyn','Queens','Bronx','Manhattan','Staten'],inplace=True)
path = os.getcwd()+'\\covid-nyc.csv'
df.to_csv(path,index=False)
