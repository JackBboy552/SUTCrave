import streamlit as st
import numpy as np
import gdown
from PIL import Image
import os
import tensorflow as tf


# Function to download .h5 file from Google Drive
def download_model():
    url = 'https://drive.google.com/drive/folders/11lpnE_iH61Q1pC4_2inhPAybpKrdF-Dx?usp=sharing'
    history_model = 'trained_model.h5'
    gdown.download(url, history_model, quiet=False)
    
    # Download labels.txt
    labels_url = 'https://drive.google.com/file/d/1-1lNkU10M8vsq3cgxUbCFSKLxRMDe9_h/view?usp=sharing'
    labels_output = 'labels.txt'
    gdown.download(labels_url, labels_output, quiet=False)

# Function to load the model
def load_model():
    model = tf.keras.models.load_model(download_model)
    return model

# Tensorflow Model Prediction
def model_prediction(model, test_image):
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(64, 64))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr]) # Convert single image to batch
    predictions = model.predict(input_arr)
    class_index = np.argmax(predictions)
    confidence = np.max(predictions) * 100  # Confidence score in percentage
    return class_index, confidence

def main():
    st.title("AI FOOD RECOGNIZE SYSTEM")

    # Download the model if it's not already downloaded
    if not os.path.exists("trained_model.h5"):
        download_model()

    # Load the model
    model = model_prediction()

    app_mode = st.sidebar.selectbox("Select Page", ["Home", "About Project", "Prediction"])

    if app_mode == "Home":
        st.header("Introduction")
        st.image("home_img.png", width=500)  # Adjust the width as needed
        
    elif app_mode == "About Project":
        st.subheader("About Dataset")
        st.text("This dataset contains images of the following food items:")
        st.code("Cuisines- ")
        st.code("Desserts- ")
        st.subheader("Content")
        st.text("This dataset contains three folders:")
        st.text("1. train (100 images each)")
        st.text("2. test (10 images each)")
        st.text("3. validation (10 images each)")

    elif app_mode == "Prediction":
        st.header("Model Prediction")
        test_image = st.file_uploader("Choose an Image:")
        
        if test_image is not None:
            if st.button("Show Image"):
                st.image(test_image, width=400, use_column_width=False)  # Adjust the width as needed

            if st.button("Predict"):
                st.success("Our Prediction")
                class_index, confidence = model_prediction(model, test_image)
                # Reading Labels
                with open("labels.txt") as f:
                    content = f.readlines()
                label = [i[:-1] for i in content]
                st.success(f"Model predicts it's a {label[class_index]} with {confidence:.2f}% confidence.")

if __name__ == "__main__":
    main()
