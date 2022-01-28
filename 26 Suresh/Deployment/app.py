
# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from sklearn.preprocessing import LabelEncoder
from collections import Counter
import pandas as pd
import numpy as np
import pickle

# Define a flask app
app = Flask(__name__)

col_list = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']

input_data = [0]*len(col_list)

# load model
dt_model = pickle.load(open('models//dt_Classifier_hc.pkl', 'rb')) 
knn_model = pickle.load(open('models//knn_Classifier_hc.pkl', 'rb')) 
lr_model = pickle.load(open('models//lr_Classifier_hc.pkl', 'rb')) 
nb_model = pickle.load(open('models//nb_Classifier_hc.pkl', 'rb')) 
rf_model = pickle.load(open('models//rf_Classifier_hc.pkl', 'rb')) 

df = pd.read_csv('csv//training.csv')
le = LabelEncoder()
df['class_prognosis'] = le.fit_transform(df['prognosis'])

print('\nModel loaded. Start serving...')
print('\nModel loaded. Check http://127.0.0.1:5000/')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symptom1 = request.form.get('symptom1')
        symptom2 = request.form.get('symptom2')
        symptom3 = request.form.get('symptom3')
        symptom4 = request.form.get('symptom4')
        symptom5 = request.form.get('symptom5')
        symptom6 = request.form.get('symptom6')
        symptoms = [symptom1, symptom2, symptom3, symptom4, symptom5, symptom6]
        for cn_ind in symptoms:
            try:
                input_data[col_list.index(cn_ind)] = 1
            except : pass

        dt_pred = dt_model.predict(np.array([input_data]))[0]
        knn_pred = knn_model.predict(np.array([input_data]))[0]
        lr_pred = lr_model.predict(np.array([input_data]))[0]
        nb_pred = nb_model.predict(np.array([input_data]))[0]
        rf_pred = rf_model.predict(np.array([input_data]))[0]
        
        output_result = [dt_pred, knn_pred, lr_pred, nb_pred, rf_pred]
        # output_result.count(output_result)
        # dict( (l, output_result.count(l) ) for l in set(output_result))

        c = Counter(output_result)
        c = c.most_common(1)[0]
        result = le.inverse_transform([c[0]])[0]
        
        return render_template('index.htm', col_list=col_list, flag=True, symptoms=symptoms, symptom1=output_result, symptom2=dict( (l, output_result.count(l) ) for l in set(output_result)), symptom3=c, result=result )    

    return render_template('index.htm', col_list=col_list, flag=False)

if __name__ == '__main__':
    app.run(debug=True)

