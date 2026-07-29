import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import os

# Variable's
model_path = os.path.join('..', 'Models', 'rf_Classifier.pkl')

# Function to load the model
@st.cache_resource
def load_model():
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    return model

# Main function for Streamlit app
def main():
    st.title("Chronic Kidney Disease Prediction")
    st.markdown("### Enter the patient details below to predict CKD status.")

    # Input fields for user
    specific_gravity = st.number_input("Specific Gravity (e.g., 1.020)", format="%.3f", min_value=1.000, max_value=1.030, step=0.001)
    albumin = st.number_input("Albumin (0-5)", min_value=0, max_value=5, step=1)
    serum_creatinine = st.number_input("Serum Creatinine (mg/dL, e.g., 1.5)", format="%.2f", min_value=0.0, step=0.1)
    haemoglobin = st.number_input("Haemoglobin (g/dL, e.g., 13.5)", format="%.1f", min_value=0.0, step=0.1)
    packed_cell_volume = st.number_input("Packed Cell Volume (e.g., 40)", min_value=0, step=1)
    red_blood_cell_count = st.number_input("Red Blood Cell Count (millions/cmm, e.g., 4.5)", format="%.2f", min_value=0.0, step=0.1)

    # Predict button
    if st.button("Predict"):
        # Load model
        model = load_model()

        # Prepare input data
        input_data = pd.DataFrame({
            "specific_gravity": [specific_gravity],
            "albumin": [albumin],
            "serum_creatinine": [serum_creatinine],
            "haemoglobin": [haemoglobin],
            "packed_cell_volume": [packed_cell_volume],
            "red_blood_cell_count": [red_blood_cell_count]
        })

        # Make prediction
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]

        # Display results
        result = "CKD " if prediction == 0 else "Not CKD "
        st.success(f"The model predicts: **{result}**")
        st.write(f"Prediction Probabilities: CKD : {probabilities[0]:.2f}, Not CKD : {probabilities[1]:.2f}")

        # Display probability graph
        st.markdown("### Probability Distribution")
        fig, ax = plt.subplots()
        ax.bar(["CKD ", "Not CKD "], probabilities, color=["red", "green"])
        ax.set_ylabel("Probability")
        ax.set_title("Prediction Probabilities")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
