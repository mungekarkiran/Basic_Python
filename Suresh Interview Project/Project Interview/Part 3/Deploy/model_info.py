import os
import re
import time
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score

STATIC_DIR = "static"
MODEL_DIR = "all_models"
STYLE_DIR = "style"
CSV_DIR = "csv"
CSV_FILE_PATH = os.path.join(STATIC_DIR, STYLE_DIR, CSV_DIR, "PersonalitySystem_test.csv")


model_list = [os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_2C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_3C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_4C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_5C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_6C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_7C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_8C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_9C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_10C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_11C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_12C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_13C.pkl'), 
              os.path.join(STATIC_DIR, MODEL_DIR, 'personality_type_model_14C.pkl')]

MinMaxScaler_path = os.path.join(STATIC_DIR, MODEL_DIR, 'MinMaxScaler_for_personality_type.pkl')

columns = ['EXT1', 'EXT2', 'EXT3', 'EXT4', 'EXT5', 'EXT6', 'EXT7', 'EXT8', 'EXT9', 'EXT10', 
           'EST1', 'EST2', 'EST3', 'EST4', 'EST5', 'EST6', 'EST7', 'EST8', 'EST9', 'EST10', 
           'AGR1', 'AGR2', 'AGR3', 'AGR4', 'AGR5', 'AGR6', 'AGR7', 'AGR8', 'AGR9', 'AGR10', 
           'CSN1', 'CSN2', 'CSN3', 'CSN4', 'CSN5', 'CSN6', 'CSN7', 'CSN8', 'CSN9', 'CSN10', 
           'OPN1', 'OPN2', 'OPN3', 'OPN4', 'OPN5', 'OPN6', 'OPN7', 'OPN8', 'OPN9', 'OPN10']

pre_info = {0:'Extroversion (E) is the personality trait of seeking fulfillment from sources outside the self or in community. High scorers tend to be very social while low scorers prefer to work on their projects alone.', 
            1:'Neuroticism (N) is the personality trait of being emotional.', 
            2:'Agreeableness (A) reflects much individuals adjust their behavior to suit others. High scorers are typically polite and like people. Low scorers tend to "tell it like it is".', 
            3:'Conscientiousness (C) is the personality trait of being honest and hardworking. High scorers tend to follow rules and prefer clean homes. Low scorers may be messy and cheat others.', 
            4:'Openness to Experience (O) is the personality trait of seeking new experience and intellectual pursuits. High scores may day dream a lot. Low scorers may be very down to earth.' }

scaled_df_columns = ["Extroversion","Neuroticism","Agreeableness","Conscientiousness","Openness"]
# ['extroversion', 'neurotic', 'agreeable', 'conscientious', 'open']


# function's
def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText

def get_silhouette_score(scaler, model, k):
    X = pd.read_csv(CSV_FILE_PATH)
    X = scaler.transform(X)
    # fit KMeans clustering model
    kmeans = KMeans(n_clusters=k, random_state=42).fit(X)
    # calculate silhouette score
    # Silhouette Coefficient: Measures how similar an object is to its own cluster compared to other clusters.
    silhouette_avg = (round(silhouette_score(X, kmeans.labels_)*100,3))
    # print("The average silhouette score is :", silhouette_avg)
    
    # Calculate Calinski-Harabasz index
    # Calinski-Harabasz Index: Measures the ratio of between-cluster variance to within-cluster variance.
    ch_score = round(calinski_harabasz_score(X, kmeans.labels_),3)
    # print("Calinski-Harabasz index:", ch_score)
    time.sleep(0.5)
    return silhouette_avg, ch_score