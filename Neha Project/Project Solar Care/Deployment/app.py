import streamlit as st
from Pages.Train_Model_Page import home_page
from Pages.Forecast_Page import forecast_page
from Pages.Classification_Page import classification_page

# Sidebar for navigation
st.sidebar.title("Solar Care")
page = st.sidebar.selectbox("Go to", ["Home - Train Your Model", "Forecast for Next 24 Hours", "Real-Time Maintenance Classification"])

# Call the selected page's function
if page == "Home - Train Your Model":
    home_page()
elif page == "Forecast for Next 24 Hours":
    forecast_page()
elif page == "Real-Time Maintenance Classification":
    classification_page()