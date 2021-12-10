import pandas as pd
import os

os.chdir('../data')

df = pd.read_csv('1RAW-DSNY_Monthly_Tonnage_Data.csv')
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

df = pd.read_csv('1RAW-DOHMH_Indoor_Environmental_Complaints.csv')
df = df.loc[df['Deleted']=='No']
df = df[['Incident_Address_Borough','Incident_Address_Zip','Date_Received']]
df.rename(columns={'Incident_Address_Borough':'Borough',
                   'Incident_Address_Zip':'zip','Date_Received':'date'}, inplace = True)
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df.dropna(inplace=True)
df.replace('Staten Island', 'Staten',inplace=True)
path = os.getcwd()+'\\indoor-complaints.csv'
df.to_csv(path,index=False)

df = pd.read_csv('1RAW-Water_Consumption_And_Cost__2013_-_2020_.csv')
df = df[['Borough','Revenue Month', 'Current Charges']]
df = df.loc[df['Borough'].isin(['BROOKLYN','QUEENS',
                                'BRONX','MANHATTAN','STATEN ISLAND'])]
df['Revenue Month'] = pd.to_datetime(df['Revenue Month'])
df['year'] = df['Revenue Month'].dt.year
df['month'] = df['Revenue Month'].dt.month
df = df.loc[df['year']>=2020]
df.rename(columns={'Current Charges':'total cost'}, inplace = True)
df.dropna(inplace=True)
df.replace(['BROOKLYN','QUEENS','BRONX','MANHATTAN','STATEN ISLAND'],
           ['Brooklyn','Queens','Bronx','Manhattan','Staten'],inplace=True)
path = os.getcwd()+'\\water-consumption.csv'
df.to_csv(path,index=False)

df = pd.read_excel('1RAW-chir_current_data.xlsx')
df = df[['Topic Area','Geographic area','Year', 'Numerator']]
df = df.loc[df['Geographic area'].isin(['Bronx County','Kings County',
                                        'New York County','Queens County',
                                        'Richmond County'])]
df['Year'] = df['Year'].str.slice(start=-4)
df.replace(',','', regex=True, inplace=True)
df['Numerator'] = df['Numerator'].apply(pd.to_numeric,errors='coerce')
df.rename(columns={'Geographic area':'Borough'}, inplace = True)
df.dropna(inplace=True)
df.replace(['Kings County','Queens County','Bronx County',
            'New York County','Richmond County'],
           ['Brooklyn','Queens','Bronx','Manhattan','Staten'],inplace=True)
path = os.getcwd()+'\\chir.csv'
df.to_csv(path,index=False)

df = pd.read_csv('1RAW-DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
df = df[['BORO','GRADE','GRADE DATE']]
df.dropna(inplace=True)
df = df.loc[df['GRADE'].isin(['A','B','C'])]
df['GRADE DATE'] = pd.to_datetime(df['GRADE DATE'])
df['year'] = df['GRADE DATE'].dt.year
df['month'] = df['GRADE DATE'].dt.month
df = df.loc[df['year']>=2020]
df.rename(columns={'BORO':'Borough','GRADE':'grade','GRADE DATE':'date'},inplace=True)
df.replace('Staten Island', 'Staten',inplace=True)
path = os.getcwd()+'\\restaurant-grade.csv'
df.to_csv(path,index=False)
