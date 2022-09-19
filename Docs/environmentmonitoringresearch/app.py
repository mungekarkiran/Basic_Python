# lib's
from flask import Flask, render_template, request
import pickle
import numpy as np
# import pyrebase
# import smtplib, ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart


# start app
app = Flask(__name__)


# config = {
#     "apiKey" : "AIzaSyB6R0ng1I3lVqNQTjwU7kzNv52919OCCLc",
#     "authDomain" : "bs-wqi.firebaseapp.com",
#     "projectId" : "bs-wqi",
#     "storageBucket" : "bs-wqi.appspot.com",
#     "messagingSenderId" : "475969977922",
#     "appId" : "1:475969977922:web:222006558f6102ee4cb7db",
#     "measurementId" : "G-FWRMRZWKPN",
#     "databaseURL" : "https://bs-wqi-default-rtdb.firebaseio.com/"
# }
# firebase = pyrebase.initialize_app(config)
# db = firebase.database()

# path of pkl file / model file.
filename = 'rf_11122020.pkl'
# load the model from disk
rf_model = pickle.load(open(filename, 'rb'))

# load models for BestUse
model_ClassA = pickle.load(open('rf_ClassA.pkl', 'rb'))
model_ClassB = pickle.load(open('rf_ClassB.pkl', 'rb'))
model_ClassC = pickle.load(open('rf_ClassC.pkl', 'rb'))
model_ClassD = pickle.load(open('rf_ClassD.pkl', 'rb'))
model_ClassE = pickle.load(open('rf_ClassE.pkl', 'rb'))

# Water Borne Disease Prediction System
bd_classA = pickle.load(open('rf_25072021_classA.pkl', 'rb'))
bd_classB = pickle.load(open('rf_25072021_classB.pkl', 'rb'))
bd_classC = pickle.load(open('rf_25072021_classC.pkl', 'rb'))
bd_classD = pickle.load(open('rf_25072021_classD.pkl', 'rb'))

allName = {
    0: "Not Suitable",
    1: "Plant",
    2: "Cold Water Fish",
    3: "Bacteria",
    4: "Bacteria & Warm Water Fish",
    5: "Bacteria & Plant",
    6: "Bacteria, Plant & Warm Water Fish",
    7: "Bacteria & Cold Water Fish",
    8: "Bacteria, Plant & Cold Water Fish"
    }

allNameInList = {
    0: ["Not_Suitable"],
    1: ["Plant"],
    2: ["Cold_Water_Fish"],
    3: ["Bacteria"],
    4: ["Bacteria", "Warm_Water_Fish"],
    5: ["Bacteria", "Plant"],
    6: ["Bacteria", "Plant", "Warm_Water_Fish"],
    7: ["Bacteria", "Cold_Water_Fish"],
    8: ["Bacteria", "Plant", "Cold_Water_Fish"]
    }

abcde_dic = {0:'F',1:'E',2:'D',3:'DE',4:'C',5:'CE',6:'CD',7:'B',8:'BE',9:'BD',10:'BDE',11:'BC',12:'BCE',13:'BCD',14:'BCDE',15:'AB',16:'ABE',17:'ABD',18:'ABDE',19:'ABC',20:'ABCE',21:'ABCD',22:'ABCDE'}

class_dic = {'A':'Class A : Drinking water source without conventional treatment but after disinfection',
             'B':'Class B : Outdoor bathing (Organised)',
             'C':'Class C : Drinking water source after conventional treatment and disinfection',
             'D':'Class D : Propagation of Wild life and Fisheries',
            'E':'Class E : Irrigation, Industrial Cooling, Controlled Waste disposal',
			'F':'Water Not suitable for Any purpose: Not meeting any of the A, B, C, D & E criteria.'}

# routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/WaterQuality', methods=['GET', 'POST'])
def WaterQuality():
	if request.method == 'POST':
		fname = request.form['FirstName']
		lname = request.form['LastName']
		Temp = request.form['Temp']
		PH = request.form['PH']
		NI_NA = request.form['NI_NA']
		DO = request.form['DO']
		prediction_value = rf_model.predict([[Temp,DO,PH,NI_NA]])

		try:
			if prediction_value >= 0 :
				return render_template('WaterQuality.html', prediction_value=allName[prediction_value[0]],
					prediction_value_allNameInList=allNameInList[prediction_value[0]])
		except Exception as e:
			pass
	return render_template('WaterQuality.html')

@app.route('/BestUse', methods=['GET','POST'])
def BestUse():
	if request.method == 'POST':
		fname = request.form['FirstName']
		lname = request.form['LastName']
		TC = request.form['TC']
		PH = request.form['PH']
		DO = request.form['DO']
		BOD = request.form['BOD']
		Amm = request.form['Amm']
		CO = request.form['CO']
		SO = request.form['SO']
		BO = request.form['BO']
		TDS = request.form['TDS']
		CH = request.form['CH']
		result = []
		val = [[float(TC), float(PH), float(DO), float(BOD), float(Amm), float(CO), float(SO), float(BO)]]
		if list(model_ClassA.predict(val))[0]:
			result.append(class_dic['A'])
		if list(model_ClassB.predict(val))[0]:
			result.append(class_dic['B'])
		if list(model_ClassC.predict(val))[0]:
			result.append(class_dic['C'])
		if list(model_ClassD.predict(val))[0]:
			result.append(class_dic['D'])
		if list(model_ClassE.predict(val))[0]:
			result.append(class_dic['E'])
		if len(result)==0:
			result.append(class_dic['F'])
		
		try:
			if len(result) >= 0 :
				return render_template('BestUse.html', ann_result=result)
		except Exception as e:
			pass
	return render_template('BestUse.html')

@app.route("/BorneDisease", methods=['GET','POST'])
def BorneDisease():
	if request.method == 'POST':
		fname = request.form['FirstName']
		lname = request.form['LastName']

		TC = request.form['TC']
		TB = request.form['TB']
		Sul = request.form['Sul']
		Alka = request.form['Alka']

		TDS = request.form['TDS']
		TSS = request.form['TSS']
		Phos = request.form['Phos']
		Cal = request.form['Cal']

		Flu = request.form['Flu']
		PH = request.form['PH']

		So = request.form['So']
		CaCo3 = request.form['CaCo3']
		Pota = request.form['Pota']

		Amm = request.form['Amm']

		Chlo = request.form['Chlo']

		Ni = request.form['Ni']

		result = []
		val = np.array([[float(TC), float(TB), float(Sul), float(Alka)]])
		y_pred_A = bd_classA.predict(val)
		if y_pred_A[0]: result.append(
			'the duration of 1 week (3 – 7 Days), you will get Gastrointestinal Diseases like Cholera / Hepatitis / Diarrhea / Taste problem and skin irritations. ')

		val = np.array([[float(TDS), float(TSS)]])
		y_pred_B = bd_classB.predict(val)
		if y_pred_B[0]: result.append(
			'the duration of 156 – 365 weeks (3 - 7 Years), you will get Kidney diseases / Hyperphosphatemi / Muscle pain / Kidney stones. ')

		val = np.array([[float(Flu), float(PH)]])
		y_pred_C = bd_classC.predict(val)
		if y_pred_C[0]: result.append('the duration of 104 - 208 weeks (2 - 4 Years), you will get Dental problems. ')

		val = np.array([[float(So), float(CaCo3)]])
		y_pred_D = bd_classD.predict(val)
		if y_pred_D[0]: result.append(
			'the duration of 156 - 520 weeks (3 - 10 Years), you will get Stroke / Heart failure / Osteoporosis / Stomach cancer / Diabetes / Reproductive failure / Neural diseases / Renal dysfunction / Hypertension. ')

		if float(Amm) == 0.5: result.append(
			'the duration of 26 - 50 weeks (6 Months – 1 Year), you will get Convulsions disease. ')

		if float(Chlo) == 250: result.append(
			'the duration of 520 - 1040 weeks (10 - 20 Years), you will get Bladder Cancer. ')

		if 300 <= float(Ni) <= 500: result.append(
			'the duration of 260 - 520 weeks (5 - 10 Years), you will get Blood Disorders (METHEMOGLOBINEMIA). ')

		print('result : ', result)

		try:
			return render_template('BorneDisease.html', result=result)
		except Exception as e:
			pass
	return render_template('BorneDisease.html')

@app.route('/Aquaponic')
def aquaponic():
    return render_template('aquaponicFarming.html')

@app.route('/FAQ')
def FAQ():
    return render_template('faq.html')

@app.route('/VideoResources')
def VideoResources():
    return render_template('videoResources.html')

@app.route('/About')
def About():
    return render_template('about.html')

# @app.route('/GetSensorData')
# def GetSensorData():
# 	my_SensorData = db.child("Sensor Data").get()
# 	my_CurrentData = db.child("Sensor Data").child("Current Value").get()
# 	return render_template('GetSensorData.html', SensorData=my_SensorData.each(), CurrentData=my_CurrentData.each(), CData=my_CurrentData.each())

if __name__ == '__main__':
    app.run(debug=True) 