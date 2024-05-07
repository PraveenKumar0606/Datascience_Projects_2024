import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score,root_mean_squared_error
import streamlit as st
from streamlit_option_menu import option_menu
import re

#page congiguration
st.set_page_config(page_title= "Retail Sales Prediction",page_icon= "random",layout= "wide",)

st.markdown("<h1 style='text-align: center; color: orange;'> Retail Weekly Sales Predicton </h1>",unsafe_allow_html=True)

selected = option_menu(None, ['HOME',"PREDICTION","DASHBOARD EDA"],
            icons=["house",'cash-coin','list-task'],orientation='horizontal',default_index=0)


if selected=='HOME':
    col1,col2 = st.columns(2)

    with col1:
        st.markdown("## :green[Technologies]")
        st.write("#### Python, Pandas, numpy, matplotlib, seaborn, Plotly, Streamlit, sklearn.")
        st.write()
        st.markdown("## :blue[Overview of the Project] ")
        st.write("#### *  Predict the weekly sales of a retail store based on historical sales using Machine Learning techniques. ")
        st.write("#### *  To perform Data cleaning, Exploratory Data Analysis and Feature Engineering for the ML model. ")
        st.write("#### *  In this use case I used the :violet[XGBoostRegressor] model to predict the weekly sales of the retail store. ")
        
    with col2:
        st.image("c:/Users/Asokamani/Pictures/Retail store.jpg",width=650)    
        st.markdown("## :red[Domain] - Retail Industry")
        
        
if selected=='PREDICTION':  
    
    # Define the possible values for the dropdown menus
    Store = [i for i in range(1, 46)] 
    Department = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
    Type = {"A":0, "B":1, "C":2}
    size=[151315, 202307,  37392, 205863,  34875, 202505,  70713, 155078,125833, 126512, 207499, 112238, 219622, 200898, 123737,  57197,93188, 120653, 203819, 203742, 140167, 119557, 114533, 128107,
          152513, 204184, 206302,  93638,  42988, 203750, 203007,  39690, 158114, 103681,  39910, 184109, 155083, 196321,  41062, 118221]
    Holiday = {"YES":1,"NO":0}
    Day_Date = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    Month_Date = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] 
    
    # Define the widgets for user input
    col1,col2,col3=st.columns([5,2,5])
    with col1:
            st.write(' ')
            store = st.selectbox('Select the **:violet[Store Number]**', Store)
            department = st.selectbox('Select the **:violet[Department Number]**', Department)
            Size = st.selectbox('Select the **:violet[Store Size]**', size)
            Temperature =st.text_input('Enter the ****:violet[Temperature]**** in fahrenheit -----> **:green[(min=5.54 & max=100.14)]**')
            Fuel_Price = st.text_input('Enter the **:violet[Fuel Price]** ---> **:green[(min=2.472 & max=4.468)]**')
            MarkDown1 = st.text_input('Enter the **:violet[Markdown1]** in dollars -------- **:green[(min=0.27,max=88646.76)]**')
            MarkDown2 = st.text_input('Enter the **:violet[Markdown2]** in dollars -------- **:green[(min=0.02,max=104519.54)]**')
            MarkDown3 = st.text_input('Enter the **:violet[Markdown3]** in dollars -------- **:green[(min=0.01,max=141630.61)]**')
            MarkDown4 = st.text_input('Enter the **:violet[Markdown4]** in dollars -------- **:green[(min=0.22,max=67474.85))]**')
            

    with col3:
                st.write(f'<h5 style="color:rgb(255, 255, 0,0.4);">NOTE: Min & Max given for reference, you can enter any value</h5>', unsafe_allow_html=True )
                MarkDown5 = st.text_input('Enter the **:violet[Markdown5]** in dollars -------- **:green[(min=135.06,max=108519.28)]**')
                CPI = st.text_input('Enter the **:violet[CPI]** ----------> **:green[(min=126.0 & max=227.47)]**')
                Unemployment = st.text_input('Enter the **:violet[Unemployment Rate]** in percentage **:green[(min=3.879 & max=14.313)]**')              
                Day_Date = st.selectbox("Select the **:violet[Date]**", Day_Date)
                Month_Date = st.selectbox("Select the **:violet[Month]**", Month_Date)
                year_date = st.text_input("Select the **:violet[Year]**")
                type = st.selectbox('Select the **:violet[Store Type]**', ['A', 'B', 'C'])
                IsHoliday = st.selectbox('Select the **:violet[Holiday]**', ["YES","NO"])
    
                   
                if st.button('Predict'):
                    Temperature=int(Temperature)
                    Fuel_Price=int(Fuel_Price)
                    MarkDown1=int(MarkDown1)
                    MarkDown2=int(MarkDown2)
                    MarkDown3=int(MarkDown3)
                    MarkDown4=int(MarkDown4)
                    MarkDown5=int(MarkDown5)
                    CPI=int(CPI)
                    Unemployment=int(Unemployment)
                    year_date=int(year_date)
        

    import pickle
    model=pickle.load(open(r'D:\Retail_Stores_Weekly_Sales_Prediction\model.pkl', 'rb'))
    result=model.predict([[store,department,Size,Temperature,Fuel_Price,MarkDown1,MarkDown2,MarkDown3,MarkDown4,MarkDown5,CPI,Unemployment,Day_Date,Month_Date,year_date,Type[type],Holiday[IsHoliday]]])

    
    predicted_price = str(result)[1:-1]
    price=result.round(2)

    st.markdown(f'<div style="background-color: yellow; border: 2px solid black; border-radius: 5px; padding: 10px; font-size: 32px; color: red;">Predicted Weekly Sales of the Retail Store is <span style="color: black;"> ${price} </span></div>', unsafe_allow_html=True) 
       

        
