import streamlit as st
from Pages.Train_Model_Page import home_page
from Pages.Forecast_Page import forecast_page

# Sidebar for navigation
st.sidebar.title("Solar Care")
page = st.sidebar.selectbox("Go to", ["Home", "Forecast"])

# Call the selected page's function
if page == "Home":
    home_page()
elif page == "Forecast":
    forecast_page()
