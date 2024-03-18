import pymysql
import pandas as pd
import streamlit as st 
from streamlit_option_menu import option_menu
import PIL
from PIL import Image
import plotly.express as px
import requests
import json


#Sql Connection
mydb=pymysql.connect(host="127.0.0.1",
                    user="root",
                    password="12345",
                    database="Phonepe",
                    port=3306)
cursor=mydb.cursor()


#aggreagated_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))


#aggreagated_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))


#aggreagated_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands",
                                        "Transaction_count","Percentage"))



#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts",
                                        "Transaction_count","Transaction_amount"))


#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","Districts",
                                        "Transaction_count","Transaction_amount"))


#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","Districts",
                                        "RegisteredUsers","AppOpens"))


#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes",
                                        "Transaction_count","Transaction_amount"))


#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes",
                                        "Transaction_count","Transaction_amount"))


#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes",
                                      "RegisteredUsers"))


# Insurance_Year
def Transaction_amount_count_Y(df, year):
    tacy= df[df["Years"]  == year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2= st.columns(2)
    with col1:

        fig_amount=px.bar(tacyg, x="States", y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(tacyg, x="States", y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Electric,height=650,width=600)
        st.plotly_chart(fig_count)
        
        
    col1,col2=st.columns(2)  
    
    with col1:
          
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states_names=[]
        for feature in data["features"]:
            states_names.append(feature["properties"]["ST_NM"])

        states_names.sort()

        fig_india=px.choropleth(tacyg, geojson=data, locations="States", featureidkey= "properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="viridis",
                                range_color= (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                height=650,width=600)
        fig_india.update_geos(visible=False)
        st.plotly_chart(fig_india)                   

    with col2:
        
        fig_india2=px.choropleth(tacyg, geojson=data, locations="States", featureidkey= "properties.ST_NM",
                            color="Transaction_count", color_continuous_scale="Rainbow",
                            range_color= (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                            hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds="locations",
                            height=650,width=600)
        fig_india2.update_geos(visible=False)
        st.plotly_chart(fig_india2) 
        
    return tacy
        
        
#Quarter        
def Transaction_amount_count_Y_Q(df,quarter):
    tacy= df[df["Quarter"]  == quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2= st.columns(2)
    
    with col1:

        fig_amount=px.bar(tacyg, x="States", y="Transaction_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        
        fig_count=px.bar(tacyg, x="States", y="Transaction_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Cividis,height=650,width=600)
        st.plotly_chart(fig_count)
    
    
    col1,col2= st.columns(2)
    
    with col1:
        
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states_names=[]
        for feature in data["features"]:
            states_names.append(feature["properties"]["ST_NM"])

        states_names.sort()

        fig_india=px.choropleth(tacyg, geojson=data, locations="States", featureidkey= "properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Electric",
                                range_color= (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                height=650,width=600)
        fig_india.update_geos(visible=False)
        st.plotly_chart(fig_india)         
                  

    with col2:
        
        fig_india2=px.choropleth(tacyg, geojson=data, locations="States", featureidkey= "properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Blues",
                                range_color= (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds="locations",
                                height=650,width=600)
        fig_india2.update_geos(visible=False)
        st.plotly_chart(fig_india2)
        
 #Transaction_type       
def Agggre_Tran_Transaction_type(df,state):
    tacy= df[df["States"]  == state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:

        fig_pie=px.pie(data_frame= tacyg, names= "Transaction_type", values="Transaction_amount", 
                        width=600, title=f" {state.upper()} TRANSACTION AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie)

    with col2:
        fig_pie_1=px.pie(data_frame= tacyg, names= "Transaction_type", values="Transaction_count", 
                        width=600, title= f"{state.upper()}TRANSACTION COUNT", hole=0.5)
        st.plotly_chart(fig_pie_1)        
        
      
#Aggregated_User_analaysis_year

def Aggre_user_plot_1(df, year):
    
    aguy=df[df["Years"] == year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")[["Transaction_count"]].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg,x ="Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy        
        
 #Aggreagated_User_State
 
def Aggre_user_plot_2(df, state):
    auys= df[df["States"] == state]
    auys.reset_index(drop=True, inplace=True)

    fig_pie_1 = px.pie(data_frame= auys, names = "Brands", values= "Transaction_count", hover_data="Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width=1000, hole=0.5)

    st.plotly_chart(fig_pie_1)
       

#Top chart     
def Top_chart_Transaction_amount(table_name):
    mydb=pymysql.connect(host="127.0.0.1",
                        user="root",
                        password="12345",
                        database="Phonepe",
                        port=3306)
    cursor=mydb.cursor()

    query1= f'''SELECT States, sum(Transaction_amount) as Transaction_Amount
                FROM {table_name}
                group by States
                order by Transaction_amount desc
                limit 10;'''
                
    cursor.execute(query1)  
    table1=cursor.fetchall() 
    mydb.commit()   

    col1,col2=st.columns(2)
    with col1:
        df_1=pd.DataFrame(table1, columns=("States","Transaction_amount"))    

        fig_amount=px.bar(df_1, x="States", y="Transaction_amount",title= "TOP 10 OF TRANSACTION AMOUNT", hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount) 


    #plot 2
    query2= f'''SELECT States, sum(Transaction_amount) as Transaction_Amount
                FROM {table_name}
                group by States
                order by Transaction_amount 
                limit 10;'''
                
    cursor.execute(query2)  
    table2=cursor.fetchall() 
    mydb.commit()   

    with col2: 
        df_2=pd.DataFrame(table2, columns=("States","Transaction_amount"))    

        fig_amount_2=px.bar(df_2, x="States", y="Transaction_amount",title= " LAST 10 OF TRANSACTION AMOUNT", hover_name="States",
                            color_discrete_sequence=px.colors.sequential.algae_r,height=650,width=600)
        st.plotly_chart(fig_amount_2) 


    #plot 3
    query3= f'''SELECT States, avg(Transaction_amount) as Transaction_Amount
                FROM {table_name}
                group by States
                order by Transaction_amount;'''
                
    cursor.execute(query3)  
    table3=cursor.fetchall() 
    mydb.commit()   


    df_3=pd.DataFrame(table3, columns=("States","Transaction_amount"))    

    fig_amount_3=px.bar(df_3, x="Transaction_amount", y="States",title= " AVG OF TRANSACTION AMOUNT", hover_name="States", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=800,width=600)
    st.plotly_chart(fig_amount_3) 
    

def Top_chart_Transaction_count(table_name):
    mydb=pymysql.connect(host="127.0.0.1",
                        user="root",
                        password="12345",
                        database="Phonepe",
                        port=3306)
    cursor=mydb.cursor()
    
    #plot 1
    query1= f'''SELECT States, sum(Transaction_count) as Transaction_count
                FROM {table_name}
                group by States
                order by Transaction_count desc
                limit 10;'''
                
    cursor.execute(query1)  
    table1=cursor.fetchall() 
    mydb.commit()   
    
    col1,col2=st.columns(2)
    
    with col1:
        df_1=pd.DataFrame(table1, columns=("States","Transaction_count"))    

        fig_amount=px.bar(df_1, x="States", y="Transaction_count",title= " TOP 10 OF TRANSACTION COUNT", hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Electric,height=650,width=600)
        st.plotly_chart(fig_amount)  


    #plot 2
    query2= f'''SELECT States, sum(Transaction_count) as Transaction_count
                FROM {table_name}
                group by States
                order by Transaction_count 
                limit 10;'''
                
    cursor.execute(query2)  
    table2=cursor.fetchall() 
    mydb.commit()   

    with col2:
        df_2=pd.DataFrame(table2, columns=("States","Transaction_count"))    

        fig_amount_2=px.bar(df_2, x="States", y="Transaction_count",title= "LAST 10 OF TRANSACTION COUNT", hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Jet_r,height=650,width=600)
        st.plotly_chart(fig_amount_2) 


    #plot 3
    query3= f'''SELECT States, avg(Transaction_count) as Transaction_count
                FROM {table_name}
                group by States
                order by Transaction_count;'''
                
    cursor.execute(query3)  
    table3=cursor.fetchall() 
    mydb.commit()   


    df_3=pd.DataFrame(table3, columns=("States","Transaction_count"))    

    fig_amount_3=px.bar(df_3, x="Transaction_count", y="States",title= "AVG OF TRANSACTION COUNT", hover_name="States", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Oranges_r,height=800,width=600)
    st.plotly_chart(fig_amount_3)    
    
#streamlit

# SETTING PAGE CONFIGURATIONS
icon = Image.open("d:\images\Phonepe symbol.jpg")
st.set_page_config(page_title= "PHONEPE DATA VISUALIZATION AND EXPLORATION | By Praveen Kumar",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded")

st.title(":rainbow[PHONEPE DATA VISUALIZATION AND EXPLORATION]")  
#Menu
with st.sidebar:
    selected = option_menu("Main Menu", ["About","Home","Explore Data","Top Charts"], 
                icons=["exclamation-circle","house","bar-chart-line","graph-up-arrow"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
    
 #Home Page
if selected == "Home":     
    col1,col2, = st.columns(2)
    col1.image(Image.open("d:\images\Phonepe_image1.png"),width =300)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("d:/images/upi.mp4")
        
        
 #Data Exploration
if selected == "Explore Data":
    Type = st.selectbox("**Type**", ("Transactions", "Users","Insurance"))
    
    if Type == "Insurance":
        
        col1,col2=st.columns(2)
        with col1:
            
             years=st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max())
        tac_Y=Transaction_amount_count_Y(Aggre_insurance,years)
        
        col1,col2=st.columns(2)
        with col1:
            Quarters =st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max())
        tac_Y_Q =Transaction_amount_count_Y_Q(tac_Y,Quarters)
        
        
    elif Type == "Transactions":
         
         col1,col2=st.columns(2)
         with col1:
            
             years=st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max())
         Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years)
        
         col1,col2=st.columns(2)
         with col1:
            Quarters =st.slider("Select The Quarter",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max())
         Aggre_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,Quarters)
           
         col1,col2=st.columns(2)
         with col1:
             states= st.selectbox("Select The States",Aggre_tran_tac_Y["States"].unique())
         Agggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)    
             
    elif Type == "Users":
         
         col1,col2=st.columns(2)
         with col1:
            
             years=st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].max())
         Aggre_user_Y=Aggre_user_plot_1(Aggre_user,years)
        
         col1,col2=st.columns(2)
         with col1:
            
             states=st.selectbox("Select The States", Aggre_user_Y["States"].unique())
             Aggre_user_s=Aggre_user_plot_2(Aggre_user_Y,states)
             
        
#Top Charts
if selected == "Top Charts":
    
    question = st.selectbox("Select the Question", 
                            ["1. What is the Transaction Amount of Aggregated Insurance", 
                             "2. What is the Transaction Count of Aggregated Insurance",
                             "3. What is the Transaction Amount of  Aggregated Transaction",
                             "4. What is the Transaction Count of  Aggregated Transaction",
                             "5. What is the Transaction Count of Aggregated User"])
         
    if question == "1. What is the Transaction Amount of Aggregated Insurance":
        
             Top_chart_Transaction_amount("aggregated_insurance")
             
    elif question == "2. What is the Transaction Count of Aggregated Insurance":
        
             Top_chart_Transaction_count("aggregated_insurance") 
             
    elif question == "3. What is the Transaction Amount of  Aggregated Transaction":
        
             Top_chart_Transaction_amount("aggregated_transaction")   
             
    elif question == "4. What is the Transaction Count of  Aggregated Transaction":
        
             Top_chart_Transaction_count("aggregated_transaction") 
             
    elif question == "5. What is the Transaction Count of Aggregated User":
        
             Top_chart_Transaction_count("aggregated_user")     
             
             
             
if selected == "About":
    col1,col2 = st.columns(2)
    with col1:
        st.video("c:/Users/Asokamani/Downloads/pulse-video.mp4")
    with col2:
        st.image(Image.open("c:/Users/Asokamani/Downloads/Phonepe_image2.png"),width = 500)
        st.subheader("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    col1,col2 = st.columns(2)
    with col1:
        st.title("THE BEAT OF PHONEPE")
        st.subheader("Phonepe became a leading digital payments company")
        st.image(Image.open("c:/Users/Asokamani/Downloads/about_phonepe.jpg"),width = 400)
        with open("c:/Users/Asokamani/Downloads/about_phonepe1.png","rb") as f:
            data = f.read()
        st.download_button("DOWNLOAD REPORT",data,file_name="annual report.pdf")
    with col2:
        st.image(Image.open("c:/Users/Asokamani/Downloads/about_phonepe1.png"),width = 800)                                             