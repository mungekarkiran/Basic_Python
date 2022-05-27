import numpy as np
import pandas as pd
pd.pandas.set_option('display.max_columns',None)

import seaborn as sns
sns.set(font_scale=1.2)

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12,8)
# %matplotlib inline

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


df = pd.read_csv(r'data/Historical Weather Data 2010-2021_preprocessed_1.csv')
# print(df.head(2).to_string())

df_with_correlation = df[['tempC_avg(0C)', 'Relative humidity_avg(%)', 'windspeedKmph_avg(Km/h)', 'pressureMB_avg', 
'precipMM_avg(mm)', 'weatherDesc', 'Sunshine Hours', '%_soil_moisure', 'Label (Disease Yes/No)']]


from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import log_loss
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import pickle

X, Y = df_with_correlation.iloc[:,:-1], df_with_correlation.iloc[:,-1]
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.3, random_state = 42, stratify = Y)


from pycaret.classification import *
clf1 = setup(data = df_with_correlation, target = 'Label (Disease Yes/No)')

# evaluate models and compare models
best = compare_models()