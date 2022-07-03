import numpy as np
import pandas as pd
pd.pandas.set_option('display.max_columns',None)

import seaborn as sns
sns.set(font_scale=1.2)

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12,8)
# %matplotlib inline

from sklearn.model_selection import train_test_split

from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import log_loss
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import hamming_loss

from sklearn.metrics import confusion_matrix

import pickle
import re

from sklearn.linear_model import LogisticRegression  
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.multioutput import MultiOutputClassifier

import docx
from docx.shared import Inches
import datetime
import os

ROOT_PATH = os.getcwd()
ARTIFACT_DIR = "Artifact"
ROOT_DIR = os.path.join(ROOT_PATH, ARTIFACT_DIR)
CURRENT_TIME_STAMP = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

MODELS_DIR = "Models"
IMAGES_DIR = "Images"
DOCS_DIR = "Docs"
LOG_DIR = "Model_Logs"
LOG_FILE_NAME = f"Log_{CURRENT_TIME_STAMP}.log"
RESULT_FILE_NAME = "MultiLabelModel_result.csv"

MODELS_DIR_PATH = os.path.join(ROOT_DIR, CURRENT_TIME_STAMP, MODELS_DIR)
IMAGES_DIR_PATH = os.path.join(ROOT_DIR, CURRENT_TIME_STAMP, IMAGES_DIR)
DOCS_DIR_PATH = os.path.join(ROOT_DIR, CURRENT_TIME_STAMP, DOCS_DIR)
LOG_DIR_PATH = os.path.join(ROOT_DIR, CURRENT_TIME_STAMP, LOG_DIR)
LOG_FILE_PATH = os.path.join(ROOT_DIR, LOG_DIR, LOG_FILE_NAME)
RESULT_FILE_PATH = os.path.join(DOCS_DIR_PATH, RESULT_FILE_NAME)

os.makedirs(MODELS_DIR_PATH, exist_ok = True)
os.makedirs(IMAGES_DIR_PATH, exist_ok = True)
os.makedirs(DOCS_DIR_PATH, exist_ok = True)
os.makedirs(LOG_DIR_PATH, exist_ok = True)


def builMultiLabelModels(X_train, y_train, classifierModel):
    
    multiLabelModel = MultiOutputClassifier(classifierModel, n_jobs=2)
    
    classifierModel = multiLabelModel.fit(X_train, y_train)
    
    y_pred = classifierModel.predict(X_train)
    
    print("Accuracy_score:", round((accuracy_score(y_train, y_pred))*100,2),'%')
    print("Loss:", round((1-accuracy_score(y_train, y_pred))*100,2),'%')
    print("Hamming_loss:", round((hamming_loss(y_train, y_pred))*100,2),'%')
    print("Classification_report:\n",metrics.classification_report(y_train, y_pred))
    
    return classifierModel, {'Accuracy': round((accuracy_score(y_train, y_pred))*100,2), 
                             'Loss': round((1-accuracy_score(y_train, y_pred))*100,2), 
                             'Hamming_loss': round((hamming_loss(y_train, y_pred))*100,2)
                            }


def fit_ensemble_voting_classifier(X_train, y_train, classifiers):
    
    # selecting top 3 models

    result_df = pd.DataFrame()

    for classifier in classifiers:
        print(f'Model : {type(classifier).__name__}')

        model, data = builMultiLabelModels(X_train, y_train, classifier)

        # save the model to disk
        FILE_NAME = f'MultiLabelModel_{type(classifier).__name__}'
        FILE_NAME = re.sub('\W+','_', FILE_NAME )+'.pkl'
        MODELS_FILE_PATH = os.path.join(MODELS_DIR_PATH, FILE_NAME)
        pickle.dump(model, open(MODELS_FILE_PATH, 'wb'))
        print(f'File saved : {MODELS_FILE_PATH}')
        
        
        data['Model_name'] = type(classifier).__name__
        data['Filename'] = MODELS_FILE_PATH

        print(f'data : {data}')

        result_df = result_df.append(data, ignore_index=True)

    result_df1 = result_df[['Model_name', 'Accuracy', 'Loss', 'Hamming_loss', 'Filename']]
    result_df1.to_csv(RESULT_FILE_PATH, index = False)

    
    

    