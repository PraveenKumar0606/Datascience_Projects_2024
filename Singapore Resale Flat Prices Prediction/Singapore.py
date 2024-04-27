import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
import streamlit as st
from streamlit_option_menu import option_menu


#page congiguration
st.set_page_config(page_title= "Singapore Resale Flat",page_icon= "🏨",layout= "wide",)

st.markdown("<h1 style='text-align: center; color: yellow;'>Singapore  Resale  Flat  Prices  Prediction</h1>",unsafe_allow_html=True)

selected = option_menu(None, ['HOME',"PREDICTION"],
            icons=["house",'cash-coin'],orientation='horizontal',default_index=0)

if selected=='HOME':
    col1,col2 = st.columns(2)

    with col1:
        st.markdown("#### :blue[**Technologies :**] Python, Pandas, Numpy, Scikit-Learn, Streamlit, Python scripting, "
                "Machine Learning, Data Preprocessing, Visualization, EDA, Model Building, Data Wrangling, "
                "Model Deployment")
        st.markdown("#### :green[**Overview :**] This project aims to construct a machine learning model and implement "
                "it as a user-friendly online application in order to provide accurate predictions about the "
                "resale values of apartments in Singapore. This prediction model will be based on past transactions "
                "involving resale flats, and its goal is to aid both future buyers and sellers in evaluating the "
                "worth of a flat after it has been previously resold. Resale prices are influenced by a wide variety "
                "of criteria, including location, the kind of apartment, the total square footage, and the length "
                "of the lease. The provision of customers with an expected resale price based on these criteria is "
                "one of the ways in which a predictive model may assist in the overcoming of these obstacles.. ")
        st.markdown("#### :red[Domain :] Real Estate")
    with col2:
        st.image("c:/Users/Asokamani/Pictures/singapore flat.jpg",use_column_width=100)
              
if selected=='PREDICTION':  
    
    # Reading cleaned data
    df=pd.read_csv("D:\Singapore Resale flat Prices\ResaleFlatPrices.csv")
      

    # Define the possible values for the dropdown menus
    Town = df['town'].unique()
    Flat_type = df['flat_type'].unique()
    Street_name = df['street_name'].unique()
    Storey_range = df['storey_range'].unique()
    Flat_model = df['flat_model'].unique()
    
    # Define the widgets for user input
    with st.form("my_form"):
        col1, col2, col3 = st.columns([5, 2, 5])
        with col1:
            st.write(' ')
            Year = st.number_input("Enter the year", value=1998, step=1)
            Town = st.selectbox("Select a Town", Town, key=1)
            Flat_type = st.selectbox('Select a Flat Type', Flat_type, key=2)
            Street_name = st.selectbox("Enter street name", Street_name, key=3)

        with col3:
            Storey_range = st.selectbox("Select a Storey Range", Storey_range, key=5)
            Floor_area_sqm = st.number_input("Enter floor area (sqm)", value=50.0, step=0.1)
            Flat_model = st.selectbox("Select a Flat Model", Flat_model, key=6)
            Lease_commence_date = st.number_input("Enter Lease commence date", value=1998, step=1)
            
            submit_button = st.form_submit_button(label="Predict Resale Price")
            st.markdown("""
                <style>
                div.stButton > button:first-child {
                    background-color: #009999;
                    color: white;
                    width: 100%;
                }
                </style>
            """, unsafe_allow_html=True)

        import pickle
        with open(r'D:\Singapore Resale flat Prices\dt.pkl', 'rb') as file:
            dt = pickle.load(file)
            
         
        ns = np.array([Town, Flat_type, Street_name, Storey_range,Floor_area_sqm, Flat_model, Lease_commence_date, Year])   
        
          # Label Encoding
        le = LabelEncoder()
        ns_encoded = le.fit_transform(ns)

        # Reshape back to the original structure
        ns_encoded = ns_encoded.reshape(1, -1)

        # Make predictions
        dt_prediction = dt.predict(ns_encoded)   
        
        #st.write('## :green[Predicted Resale Price:] ',f"$ {dt_prediction}")
        st.markdown(f'<div style="background-color: white; border: 2px solid black; border-radius: 5px; padding: 10px; font-size: 32px; color: red;">Predicted Resale Price: <span style="color: darkgreen;"> ${dt_prediction} </span></div>', unsafe_allow_html=True)    
        

       
