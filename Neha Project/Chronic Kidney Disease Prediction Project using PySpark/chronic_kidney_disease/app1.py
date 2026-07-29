import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/kidney_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('KidneyDiseaseApp')

class KidneyDiseaseApp:
    def __init__(self, model_path):
        """Initialize the Streamlit app with the trained model"""
        try:
            # Initialize Spark session
            self.spark = SparkSession.builder \
                .appName("KidneyDiseasePredictionApp") \
                .getOrCreate()
            
            # Load the trained model
            self.model = PipelineModel.load(model_path)
            
            logger.info("App initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize app: {str(e)}")
            raise

    def preprocess_input(self, input_data):
        # """Preprocess user input to match model requirements"""
        # try:
        #     # Convert input data to Spark DataFrame
        #     input_df = self.spark.createDataFrame(input_data)
        #     logger.info("Input data converted to Spark DataFrame")
        #     return input_df
        # except Exception as e:
        #     logger.error(f"Error preprocessing input: {str(e)}")
        #     raise
        """Preprocess user input using the saved preprocessing pipeline"""
        try:
            # Convert input data to Spark DataFrame
            input_df = self.spark.createDataFrame(input_data)
            logger.info("Input data converted to Spark DataFrame")
            
            # Ensure all numeric fields are properly typed
            numeric_cols = ['age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 
                        'sc', 'sod', 'pot', 'hemo', 'pcv', 'wbcc', 'rbcc']
            for col in numeric_cols:
                if col in input_df.columns:
                    input_df = input_df.withColumn(col, input_df[col].cast("double"))
            
            # Apply the preprocessing pipeline
            if hasattr(self, 'preprocessor'):
                processed_df = self.preprocessor.transform(input_df)
                logger.info("Input data preprocessing completed")
                return processed_df
            else:
                raise AttributeError("Preprocessor not loaded. Call load_model() first")
                
        except Exception as e:
            logger.error(f"Error preprocessing input: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to preprocess input: {str(e)}") from e


    def predict(self, input_df):
        """Make prediction using the trained model"""
        try:
            # Make prediction
            predictions = self.model.transform(input_df)
            
            # Extract probability and prediction
            prediction = predictions.collect()[0]
            probability = prediction["probability"][1]  # Probability of class 1 (CKD)
            
            logger.info(f"Prediction made successfully: {probability:.4f}")
            return probability, prediction["prediction"]
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise

    def run(self):
        """Run the Streamlit application"""
        try:
            st.title("Chronic Kidney Disease Prediction")
            st.write("""
            This app predicts the likelihood of a patient having Chronic Kidney Disease (CKD)
            based on clinical parameters. Please fill in the patient details below.
            """)
            
            # Create input form
            with st.form("patient_details"):
                st.header("Patient Information")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    age = st.number_input("Age", min_value=1, max_value=120, value=50)
                    bp = st.number_input("Blood Pressure (mm Hg)", min_value=50, max_value=250, value=80)
                    sg = st.selectbox("Specific Gravity", [1.005, 1.010, 1.015, 1.020, 1.025])
                    al = st.selectbox("Albumin (0-5)", [0, 1, 2, 3, 4, 5])
                    su = st.selectbox("Sugar (0-5)", [0, 1, 2, 3, 4, 5])
                    rbc = st.selectbox("Red Blood Cells", ["normal", "abnormal"])
                    pc = st.selectbox("Pus Cells", ["normal", "abnormal"])
                    
                with col2:
                    pcc = st.selectbox("Pus Cell Clumps", ["present", "notpresent"])
                    ba = st.selectbox("Bacteria", ["present", "notpresent"])
                    bgr = st.number_input("Blood Glucose Random (mg/dL)", min_value=50, max_value=500, value=100)
                    bu = st.number_input("Blood Urea (mg/dL)", min_value=10, max_value=300, value=40)
                    sc = st.number_input("Serum Creatinine (mg/dL)", min_value=0.5, max_value=20.0, value=1.0)
                    sod = st.number_input("Sodium (mEq/L)", min_value=100, max_value=200, value=140)
                    pot = st.number_input("Potassium (mEq/L)", min_value=2.0, max_value=10.0, value=4.0)
                
                hemo = st.number_input("Hemoglobin (g/dL)", min_value=3.0, max_value=20.0, value=12.0)
                pcv = st.number_input("Packed Cell Volume", min_value=10, max_value=60, value=40)
                wbcc = st.number_input("White Blood Cell Count (cells/cumm)", min_value=2000, max_value=20000, value=8000)
                rbcc = st.number_input("Red Blood Cell Count (millions/cmm)", min_value=2.0, max_value=8.0, value=4.5)
                htn = st.selectbox("Hypertension", ["yes", "no"])
                dm = st.selectbox("Diabetes Mellitus", ["yes", "no"])
                cad = st.selectbox("Coronary Artery Disease", ["yes", "no"])
                appet = st.selectbox("Appetite", ["good", "poor"])
                pe = st.selectbox("Pedal Edema", ["yes", "no"])
                ane = st.selectbox("Anemia", ["yes", "no"])
                
                submitted = st.form_submit_button("Predict")
            
            if submitted:
                # Prepare input data
                input_data = [{
                    "age": float(age),
                    "bp": float(bp),
                    "sg": float(sg),
                    "al": float(al),
                    "su": float(su),
                    "rbc": rbc,
                    "pc": pc,
                    "pcc": pcc,
                    "ba": ba,
                    "bgr": float(bgr),
                    "bu": float(bu),
                    "sc": float(sc),
                    "sod": float(sod),
                    "pot": float(pot),
                    "hemo": float(hemo),
                    "pcv": float(pcv),
                    "wbcc": float(wbcc),
                    "rbcc": float(rbcc),
                    "htn": htn,
                    "dm": dm,
                    "cad": cad,
                    "appet": appet,
                    "pe": pe,
                    "ane": ane
                }]
                
                try:
                    # Preprocess and predict
                    input_df = self.preprocess_input(input_data)
                    probability, prediction = self.predict(input_df)
                    
                    # Display results
                    st.subheader("Prediction Results")
                    st.write(f"Probability of Chronic Kidney Disease: {probability:.2%}")
                    
                    if prediction == 1:
                        st.error("Prediction: Chronic Kidney Disease (Positive)")
                        st.warning("Please consult a nephrologist for further evaluation.")
                    else:
                        st.success("Prediction: No Chronic Kidney Disease (Negative)")
                        st.info("Maintain a healthy lifestyle with regular checkups.")
                    
                    # Show interpretation
                    st.subheader("Interpretation")
                    st.write("""
                    - **Probability > 70%**: High likelihood of CKD
                    - **Probability 30-70%**: Moderate likelihood, further tests recommended
                    - **Probability < 30%**: Low likelihood of CKD
                    """)
                    
                except Exception as e:
                    st.error("An error occurred during prediction. Please try again.")
                    logger.error(f"Prediction error: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error running Streamlit app: {str(e)}")
            st.error("A critical error occurred. Please check the logs.")
        finally:
            self.spark.stop()
            logger.info("Spark session stopped")

if __name__ == "__main__":
    try:
        # Find the latest model
        model_dir = "models"
        model_files = [f for f in os.listdir(model_dir) if f.startswith("kidney_model")]
        if not model_files:
            st.error("No trained model found. Please train the model first.")
            exit()
        
        # Get the most recent model
        latest_model = sorted(model_files)[-1]
        model_path = os.path.join(model_dir, latest_model)
        
        logger.info(f"Loading model from {model_path}")
        app = KidneyDiseaseApp(model_path)
        app.run()
    except Exception as e:
        logger.error(f"Fatal error in app initialization: {str(e)}")
        st.error("Failed to initialize the application. Please check the logs.")