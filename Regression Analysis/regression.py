import os
import sys
import pandas as pd
import scipy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from dataloading import dataloader
import statsmodels.api as sm

Boroughs = ['Manhattan','Queens','Brooklyn','Bronx','Staten']
df_dict = dataloader(['restaurant','covid'])
df_rest = df_dict['restaurant']
df_covid = df_dict['covid']
new_case_by_month = df_covid[['year','month','Borough','New Positives']].groupby(by=['year','month','Borough']).sum()

ALL_GRADES = pd.DataFrame()

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

    grades = grades.transpose()
    grades['NP'] = np.array(covid_counts)
    ALL_GRADES = pd.concat([ALL_GRADES,grades])

ALL_GRADES = ALL_GRADES.fillna(0)

# Multivariate Linear Regression based on Restaurant Grades
print("Multivariate Linear Regression:")
x = ALL_GRADES[['A','B','C']]
y = ALL_GRADES[['NP']]
model = LinearRegression().fit(x,y)
r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)
print('intercept:', model.intercept_)
print('slope:', model.coef_)

# Polynomial Regression
print("\nPolynomial Regression of degree 2:")
x_ = PolynomialFeatures(degree=2, include_bias=False).fit_transform(x)
model2 = LinearRegression().fit(x_, y)
r_sq = model2.score(x_, y)
print('coefficient of determination:', r_sq)
print('intercept:', model2.intercept_)
print('slope:', model2.coef_)

# Polynomial Regression
print("\nPolynomial Regression of degree 3:")
x_3 = PolynomialFeatures(degree=3, include_bias=False).fit_transform(x)
model3 = LinearRegression().fit(x_3, y)
r_sq = model3.score(x_3, y)
print('coefficient of determination:', r_sq)
print('intercept:', model3.intercept_)
print('slope:', model3.coef_)

# Ordinary Least Square Regression
print("\nOLS Regression:")
x_4 = sm.add_constant(x)
model4 = sm.OLS(y, x_4)
results = model4.fit()
print('coefficient of determination:', results.rsquared)
print('adjusted coefficient of determination:', results.rsquared_adj)
print('regression coefficients:', results.params)

# Ridge Regression
print('\nRidge Regression:')
modelR = Ridge(alpha=0.5)
modelR.fit(x, y)
r_sq = modelR.score(x, y)
print('coefficient of determination:', r_sq)
print('intercept:', modelR.intercept_)
print('slope:', modelR.coef_)
