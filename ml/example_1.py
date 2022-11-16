# This is an extremely simple regression model that predicts 'Life satisfaction'
# from GDP. It is not a serious model. I wrote it only to learn the modelling
# steps in Scikit-Learn.

# The example is taken from the book 'Hands-On Machine Learning with
# Scikit-Learn and TensorFlow' by Aurelien Geron. The code is not the same as
# in the book although the model is identical.

import numpy as np
import matplotlib.pyplot as ply
import pandas as pd
from sklearn.linear_model import LinearRegression

oecd_file = "data\\OECD_data.tsv"
imf_file = "data\\BLI_16112022194309139.csv"

oecd_data = pd.read_csv(oecd_file, delimiter='\t')
imf_data = pd.read_csv(imf_file)

# Clean GDP data.
gdp_data = oecd_data.loc[:, ['Country', '2022']]
gdp_data = gdp_data.rename(columns={'2022': 'gdp'})
gdp_data.loc[gdp_data['gdp'] == '--', 'gdp'] = '0'
gdp_data.loc[gdp_data['gdp'] == 'na', 'gdp'] = '0'
gdp_data.loc[gdp_data['gdp'] == 'n/a', 'gdp'] = '0'
gdp_data.gdp = gdp_data.gdp.str.replace(',', '').astype('float')

# Extract life satisfaction data.
happiness = imf_data.loc[imf_data['Indicator'] == 'Life satisfaction',
                         ['Country', 'Value']]
# There are multiple rows for a single country. We will use the mean value of
# 'Life satisfaction'.
happiness_agg = happiness.groupby('Country').mean()

model_data = pd.merge(left=gdp_data, right=happiness, how='inner', on='Country')

model = LinearRegression()
X = model_data.loc[:, ['gdp']].to_numpy()
y = model_data.loc[:, ['Value']].to_numpy()
model.fit(X, y)

cyprus_gdp = 22587
cyprus_happiness = np.round(model.predict([[cyprus_gdp]])[0][0], 2)

print("Cyprus GDP = {}, predicted happiness = {}.".format(cyprus_gdp,
                                                          cyprus_happiness))
