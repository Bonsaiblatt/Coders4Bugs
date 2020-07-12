import pandas as pd
from os import listdir
import matplotlib.pyplot as plt
from pathlib import Path
from functools import reduce
import numpy as np
import pickle

# Look for all files in the image
path = Path('data/sat_data')
file_list = listdir(path)
file_location = [path / i for i in file_list]

csv_list = []

# Read all bands as pd dataframe
for i in file_list:
    csv_list.append(pd.read_csv(path / i, skiprows=2, sep='\t', header=None, names=['ID', i[:-4]]))

# Join dataframesl, drop ID and rescale
df = reduce(lambda left,right: pd.merge(left,right,on='ID'), csv_list)
df = df.drop('ID', axis=1)
df = df / 10000

# Calculate indices
df['BI'] = np.sqrt((df.B4**2 + df.B3**2)/2)
df['BI2'] = np.sqrt((df.B4**2 + df.B3**2 + df.B8**2) / 3)
df['CI'] = (df.B4 - df.B3) / (df.B4 + df.B3)
df['GNDVI'] = (df.B8 - df.B3) / (df.B8 + df.B3)
df['NDVI'] = (df.B8 - df.B4) / (df.B8 + df.B4)
df['WDVI'] = (df.B8 - (df.B8 / df.B4)) * df.B4
L = 1 - (2 * df['NDVI'] * df['WDVI'])
df['MSAVI'] = (1+L)*(df.B8 - df.B4) / (df.B8 + df.B4 + L)
df['MSAVI2'] = (2 * df.B8+ 1 - np.sqrt((2*df.B8+1)**2 - 8 * (df.B8 - df.B4)))/2
df['RI'] = df.B4**2 / df.B3**3
df['SAVI'] = ((df.B8 - df.B4)* 1.5 )/( df.B8 - df.B4 + 0.5)
df['TSAVI'] = (df.B8 - df.B4)/ (df.B4 + 0.08)
df['LAI'] = 10.22 * df.WDVI + 0.4768

# Todo: Remove when B9 data is calcualted
# df['B9'] = df.B8A

# Order the dataframe
df_ordered = df[['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12', 'BI', 'BI2', 'CI', 'GNDVI',
                 'MSAVI', 'MSAVI', 'NDVI', 'RI', 'SAVI', 'TSAVI', 'WDVI', 'LAI']]

# Read the model
with open(Path('data/model_v1.pkl'), 'rb') as file:
    svr_model = pickle.load(file)

predictions = svr_model.predict(df_ordered)
image = predictions.reshape(168, 106)

fig = plt.figure()
plt.imshow(image, cmap='jet')
plt.colorbar(label='Pb (mg/Kg)')
plt.xlabel('Pixel (20m)')
plt.ylabel('Pixel (20m)')
plt.savefig(Path('media/result.jpeg'))



