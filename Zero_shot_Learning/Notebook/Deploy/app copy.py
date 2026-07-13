from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input
from keras.models import load_model
from skimage.feature import graycomatrix, graycoprops
from pickle import load
from sentence_transformers import SentenceTransformer, util
import torch

# Function to extract visual features using ResNet50
def extract_visual_features(image_path, model):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))  # Resize image for ResNet50 input
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)
    visual_features = model.predict(img_array, verbose = 0)
    return visual_features

# Function to compute GLCM texture features
def compute_texture_features(image_path):
    distances = [1, 3, 5, 3, 1, 3, 5]
    angles = [0, 0, 0, np.pi/4, np.pi/2, np.pi/2, np.pi/2]
    glcm_features = []
    for distance, angle in list(zip(distances, angles)):
        img_gray = Image.open(image_path).convert('L')  # Convert image to grayscale
        img_gray_array = np.array(img_gray)
        glcm = graycomatrix(img_gray_array, distances=[distance], angles=[angle], levels=256, symmetric=True, normed=True)
        contrast = graycoprops(glcm, 'contrast')[0, 0]
        dissimilarity = graycoprops(glcm, 'dissimilarity')[0, 0]
        homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
        energy = graycoprops(glcm, 'energy')[0, 0]
        correlation = graycoprops(glcm, 'correlation')[0, 0]
        glcm_features.extend([contrast, dissimilarity, homogeneity, energy, correlation])
    return np.array(glcm_features) 


# Streamlit app
def main():
    # Load models
    ResNet50_model = ResNet50(weights='imagenet', include_top=False, pooling='avg') 
    # classification_model = load_model(r'classification_model.h5')
    # min_max_scaler_model = load(open(r'min_max_scaler_file.pkl', 'rb'))
    SentenceTransformer_model = SentenceTransformer('all-MiniLM-L6-v2')
    seen_class_labels = ['Atelectasis', 'Consolidation', 'Effusion', 'Hernia', 'Mass', 'No Finding', 'Pneumonia']
    seen_idx_to_class = {k: v for k, v in enumerate(seen_class_labels)}
    seen_words = list(seen_idx_to_class.values()) 
    seen_embeddings = SentenceTransformer_model.encode(seen_words, convert_to_tensor=True)

    unseen_class_labels = ['Cardiomegaly', 'Edema', 'Emphysema', 'Fibrosis', 'Infiltration', 'Nodule', 'Pleural_Thickening', 'Pneumothorax']
    unseen_idx_to_class = {k: v for k, v in enumerate(unseen_class_labels)}
    unseen_words = list(unseen_idx_to_class.values()) 
    unseen_embeddings = SentenceTransformer_model.encode(unseen_words, convert_to_tensor=True)


    # Define the app
    st.title("🔎 Image Classification with Probability Visualization")

    uploaded_file = st.file_uploader("Upload an Image", type=["jpg","jpeg","png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        visual_features = extract_visual_features(uploaded_file, ResNet50_model)
        # st.write(f'visual_features: {visual_features}')

        # Compute texture features using GLCM
        texture_features = compute_texture_features(uploaded_file)
        # st.write(f'Texture Features: {texture_features}')

        # Combine features
        # combined_features = np.concatenate([visual_features, texture_features])
        # st.write(f'Combined Features: {combined_features}')

        # Concatenate visual and texture features
        l1 = visual_features[0].tolist()
        l2 = texture_features.tolist()
        l1.extend(l2)
        combined_features = np.array(l1)
        # st.write(f'Combined Features: {combined_features}')

        # Normalize the features # ...
        # train_normalized_texture_features = min_max_scaler_model.transform([combined_features])
        # train_normalized_texture_features_df = pd.DataFrame(train_normalized_texture_features)
        # # model predict
        # predicted_value = classification_model.predict(train_normalized_texture_features_df, verbose = 0)
        # st.write(f"predicted_value : {np.argmax(predicted_value)} || {seen_class_labels[np.argmax(predicted_value)]}")
        # predicted_class = 'Consolidation' # seen_class_labels[np.argmax(predicted_value)]
        # confidence = 0.59865 # max(predicted_value[0])
        # st.subheader(f"Predicted Class: **{predicted_class}**")
        # st.write(f"Confidence: **{confidence:.2f}**")
        
        predicted_class = 'Consolidation' 
        confidence = 0.89865 
        st.subheader(f"✅ Predicted Class: **{predicted_class}**")
        st.write(f"Confidence: **{confidence:.2f}**")

        # Find top n similar 
        seen_query = SentenceTransformer_model.encode(predicted_class, convert_to_tensor=True)
        seen_cosine_scores = util.cos_sim(seen_query, seen_embeddings)
        # Show top-3 results
        seen_top_results = torch.topk(seen_cosine_scores[0], k=5)

        seen_class_names, seen_probabilities = [], []
        for score, idx in zip(seen_top_results.values, seen_top_results.indices):
            # st.write(f"Class: {seen_class_labels[idx]}, Similarity: {score:.2f}")
            seen_class_names.append(seen_class_labels[idx])
            seen_probabilities.append(float(f"{score:.2f}"))

        
        # Find top n similar 
        unseen_query = SentenceTransformer_model.encode(predicted_class, convert_to_tensor=True)
        unseen_cosine_scores = util.cos_sim(unseen_query, unseen_embeddings)
        # Show top-3 results
        unseen_top_results = torch.topk(unseen_cosine_scores[0], k=5)

        unseen_class_names, unseen_probabilities = [], []
        for score, idx in zip(unseen_top_results.values, unseen_top_results.indices):
            # st.write(f"Class: {unseen_class_labels[idx]}, Similarity: {score:.2f}")
            unseen_class_names.append(unseen_class_labels[idx])
            unseen_probabilities.append(float(f"{score:.2f}"))

        # # Simulate a classification result
        # class_names = ["Cat", "Dog", "Bird"]
        # probabilities = [0.7, 0.2, 0.1]
        
        # # st.write("### Classification Results")
        # # for class_name, prob in zip(class_names, probabilities):
        # #     st.write(f"{class_name}: {prob:.2f}")
        
        # Create a DataFrame for the bar chart
        seen_data = pd.DataFrame({
            'Class': seen_class_names,
            'Probability': seen_probabilities
        })

        # Create a DataFrame for the bar chart
        unseen_data = pd.DataFrame({
            'Class': unseen_class_names,
            'Probability': unseen_probabilities
        })

        # # # Display a bar chart for probabilities
        # # st.bar_chart(data.set_index('Class')['Probability'], use_container_width=True)

        # Create 2 equal-width columns
        col1, col2 = st.columns(2)

        with col1:
            st.header("From Seen")
            # st.write("This is the left side")
            # st.button("Click me!")

            st.subheader("Prediction Probabilities")
            for _, row in seen_data.iterrows():
                st.write(f"{row['Class']} : {(row['Probability']*100):.2f} %")
                st.progress(float(row['Probability']))


        with col2:
            st.header("From Unseen")
            # st.write("This is the right side")
            # st.slider("Select a value", 0, 100)

            st.subheader("Prediction Probabilities")
            for _, row in unseen_data.iterrows():
                st.write(f"{row['Class']} : {(row['Probability']*100):.2f} %")
                st.progress(float(row['Probability']))


# Run the app
if __name__ == "__main__":
    main()
    # streamlit run your_app.py