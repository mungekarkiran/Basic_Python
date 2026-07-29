# app.py
import streamlit as st
import pandas as pd
import logging
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
import sys

# Configure logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{log_dir}/kidney_app_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("KidneyDiseaseApp")

class KidneyDiseaseApp:
    def __init__(self):
        """Initialize the Streamlit app and Spark session"""
        try:
            # Configure Spark for Windows if needed
            # if sys.platform.startswith('win'):
            #     os.environ['HADOOP_HOME'] = "C:\\hadoop"  # Update if different
            #     os.environ['PATH'] = f"{os.environ['HADOOP_HOME']}\\bin;{os.environ['PATH']}"
            #     os.environ['PYSPARK_PYTHON'] = sys.executable
            #     os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

            # Initialize Spark session
            # self.spark = SparkSession.builder \
            #     .appName("KidneyDiseasePredictionApp") \
            #     .config("spark.executor.memory", "2g") \
            #     .config("spark.driver.memory", "2g") \
            #     .getOrCreate()
            self.spark = SparkSession.builder \
                .config("spark.driver.host", "localhost") \
                .appName("KidneyDiseasePredictionApp") \
                .getOrCreate()
            logger.info("Spark session initialized successfully")

            # Load model (will be set in load_model())
            self.pipeline_model = None
            self.model_loaded = False

            logger.info("App initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize app: {str(e)}", exc_info=True)
            raise

    def load_model(self, model_path):
        """Load the trained pipeline model"""
        try:
            logger.info(f"Loading model from {model_path}")
            self.pipeline_model = PipelineModel.load(model_path)
            self.model_loaded = True
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}", exc_info=True)
            st.error("Failed to load prediction model. Please check the logs.")
            raise

    def preprocess_input(self, input_data):
        """Preprocess user input using the pipeline"""
        try:
            # Convert to Spark DataFrame
            input_df = self.spark.createDataFrame(input_data)
            
            # Apply the full pipeline (preprocessing + model)
            processed_df = self.pipeline_model.transform(input_df)
            
            return processed_df
        except Exception as e:
            logger.error(f"Error preprocessing input: {str(e)}", exc_info=True)
            raise

    def predict(self, input_data):
        """Make prediction on input data"""
        try:
            if not self.model_loaded:
                raise ValueError("Model not loaded")
                
            # Preprocess and predict
            processed_df = self.preprocess_input(input_data)
            prediction = processed_df.collect()[0]
            
            return {
                'prediction': int(prediction['prediction']),
                'probability': float(prediction['probability'][1]),  # Probability of CKD
                'raw_prediction': [float(x) for x in prediction['rawPrediction']]
            }
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}", exc_info=True)
            raise

    def create_input_form(self):
        """Create the Streamlit input form"""
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
                sc = st.number_input("Serum Creatinine (mg/dL)", min_value=0.5, max_value=20.0, value=1.0, step=0.1)
                sod = st.number_input("Sodium (mEq/L)", min_value=100, max_value=200, value=140)
                pot = st.number_input("Potassium (mEq/L)", min_value=2.0, max_value=10.0, value=4.0, step=0.1)
            
            hemo = st.number_input("Hemoglobin (g/dL)", min_value=3.0, max_value=20.0, value=12.0, step=0.1)
            pcv = st.number_input("Packed Cell Volume", min_value=10, max_value=60, value=40)
            wbcc = st.number_input("White Blood Cell Count (cells/cumm)", min_value=2000, max_value=20000, value=8000)
            rbcc = st.number_input("Red Blood Cell Count (millions/cmm)", min_value=2.0, max_value=8.0, value=4.5, step=0.1)
            htn = st.selectbox("Hypertension", ["yes", "no"])
            dm = st.selectbox("Diabetes Mellitus", ["yes", "no"])
            cad = st.selectbox("Coronary Artery Disease", ["yes", "no"])
            appet = st.selectbox("Appetite", ["good", "poor"])
            pe = st.selectbox("Pedal Edema", ["yes", "no"])
            ane = st.selectbox("Anemia", ["yes", "no"])
            
            submitted = st.form_submit_button("Predict")
            
            if submitted:
                return {
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
                }
        return None

    def display_results(self, result):
        """Display prediction results"""
        st.subheader("Prediction Results")
        
        # Prediction and probability
        if result['prediction'] == 1:
            st.error("**Prediction:** Chronic Kidney Disease (Positive)")
        else:
            st.success("**Prediction:** No Chronic Kidney Disease (Negative)")
        
        st.write(f"**Probability of CKD:** {result['probability']:.1%}")
        
        # Interpretation
        st.subheader("Interpretation")
        if result['probability'] > 0.7:
            st.warning("High likelihood of CKD. Please consult a nephrologist immediately.")
        elif result['probability'] > 0.3:
            st.warning("Moderate likelihood of CKD. Further tests recommended.")
        else:
            st.info("Low likelihood of CKD. Maintain regular checkups.")
        
        # Debug info (can be hidden in production)
        with st.expander("Advanced Details"):
            st.write("Raw prediction values:", result['raw_prediction'])
            st.write("""
            **Classification Threshold:** 0.5  
            **Prediction Meaning:**  
            - 0 = No Chronic Kidney Disease  
            - 1 = Chronic Kidney Disease
            """)

    def run(self):
        """Run the Streamlit application"""
        try:
            st.set_page_config(
                page_title="Chronic Kidney Disease Prediction",
                page_icon="🩺",
                layout="wide"
            )
            
            st.title("Chronic Kidney Disease Prediction")
            st.write("""
            This app predicts the likelihood of a patient having Chronic Kidney Disease (CKD)
            based on clinical parameters. Please fill in the patient details below.
            """)
            
            # Load model (update path as needed)
            model_path = "models/kidney_model"  # Update with your model path
            if not hasattr(self, 'pipeline_model'):
                self.load_model(model_path)
            
            # Create input form
            input_data = self.create_input_form()
            
            if input_data:
                try:
                    # Make prediction
                    result = self.predict([input_data])  # Wrap in list for single prediction
                    self.display_results(result)
                    
                    # Log successful prediction (without PHI)
                    logger.info("Prediction made successfully")
                except Exception as e:
                    st.error("An error occurred during prediction. Please try again.")
                    logger.error(f"Prediction error: {str(e)}", exc_info=True)
            
        except Exception as e:
            st.error("A critical error occurred. Please check the application logs.")
            logger.critical(f"Application error: {str(e)}", exc_info=True)
        finally:
            if hasattr(self, 'spark'):
                self.spark.stop()
                logger.info("Spark session stopped")

if __name__ == "__main__":
    try:
        logger.info("Starting Streamlit application")
        app = KidneyDiseaseApp()
        app.run()
    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}", exc_info=True)
        st.error("Failed to initialize the application. Please check the logs.")