import pandas as pd
import pymongo
import streamlit as st 
from streamlit_option_menu import option_menu
import plotly_express as px
from PIL import Image


# page configuration
page_icon_url = (r'c:\Users\Asokamani\Pictures\Airbnb_logo.png')
st.set_page_config(page_title='Airbnb',page_icon=page_icon_url, layout="wide")


# title and position
st.markdown(f'<h1 style="text-align: center;color:red;">Airbnb Analysis</h1>',
                unsafe_allow_html=True)


with st.sidebar:
    image_url = (r'c:\Users\Asokamani\Pictures\airnbnb banner.jpg')
    st.image(image_url, use_column_width=True)

    option = option_menu(menu_title='Main_menu', options=['Home', 'Features Analysis'],
                         icons=['database-fill', 'list-task'])
    col1, col2 = st.columns([0.30, 0.48])
    
    
# READING THE CLEANED DATAFRAME
df = pd.read_csv(r'D:\AirBnb Analysis\Airbnb_data.csv')    


if option == "Home":

 st.subheader("Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.")
 st.subheader(':green[Skills take away From This Project]:')
 st.subheader('Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI or Tableau')
 st.subheader(':blue[Domain]:')
 st.subheader('Travel Industry, Property management and Tourism')
 
 
df = pd.read_csv(r'D:\AirBnb Analysis\Airbnb_data.csv')
country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))


if option=="Features Analysis":
    
  df = pd.read_csv(r'D:\AirBnb Analysis\Airbnb_data.csv')
  
   # CONVERTING THE USER INPUT INTO QUERY  
  query = f'Country in {country} & Room_type in {room} & Property_type in {prop}'

  col1,col2=st.columns([1,1],gap='small')

  with col1:
      
        df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="count").sort_values(by='count',ascending=False)[:10]
        fig = px.bar(df1,
                         title='Top 10 Property Types With Count',
                         x='Property_type',
                         y='count',
                         orientation='v',
                         color='Property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True) 
        
        
        df1= df.query(query).groupby(["Room_type"]).size().reset_index(name="count").sort_values(by='count',ascending=False)[:10]
        fig = px.pie(df1,
                             title=' Room_Type With Count',
                             values='count',
                             names="Room_type")
        fig.update_traces(textposition='inside', textinfo='value+label')
        st.plotly_chart(fig,use_container_width=True)    
        
        
        df1= df.query(query).groupby(["Bed_type"]).size().reset_index(name="count").sort_values(by='count',ascending=False)[:10]
        fig = px.line(df1,
                             title=' Bed_Type With Count',
                             x='Bed_type',
                             y='count',text='count',markers=True)
        fig.update_traces(textposition="top center")                    
        st.plotly_chart(fig,use_container_width=True)
        
        
        df1= df.query(query).groupby(["Cancellation_policy"]).size().reset_index(name="count").sort_values(by='count',ascending=False)[:10]
        fig = px.line(df1,
                             title=' Cancellation_Policy With Count',
                             x='Cancellation_policy',
                             y='count',text='count',markers=True)

        fig.update_traces(textposition="top center")                    
        st.plotly_chart(fig,use_container_width=True)
        
        
        df1= df.query(query).groupby(["No_of_reviews"]).size().reset_index(name="count").sort_values(by='count',ascending=False)[:10]
        fig = px.bar(df1,
                             title=' Number_Of_Reviews With Count',
                             x="No_of_reviews",
                             y="count",
                             text="count",
                             orientation='v',
                             color='count',
                             color_continuous_scale=px.colors.sequential.Darkmint_r)
        fig.update_traces( textposition='outside')
        st.plotly_chart(fig,use_container_width=True)
        
        
  with col2: 
      
        df1= df1= df.query(query).groupby('Room_type',as_index=False)['Min_nights'].sum()
        fig = px.pie(df1,
                             title='Minimum_Nights With Room_Type',
                             values="Min_nights",
                             names="Room_type")
        fig.update_traces(textposition='inside', textinfo='value+label')
        st.plotly_chart(fig,use_container_width=True) 
        
        
        df1= df1= df.query(query).groupby(["Max_nights"]).size().reset_index(name="count").sort_values(by='count',ascending=False)[:10]
        fig = px.pie(df1,
                             title='Maximum_Nights With Count',
                             values='count',
                             names="Max_nights")
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12)
        st.plotly_chart(fig,use_container_width=True)
        
        
        df1= df1= df.query(query).groupby(["Accomodates"]).size().reset_index(name="count").sort_values(by='count',ascending=False)[:10]
        fig = px.bar(df1,
                             title='Accommodates With Count',
                             x="Accomodates",
                             y="count",
                             orientation='v',
                             color='count',
                             color_continuous_scale=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig,use_container_width=True)
        
        
        df1= df1= df.query(query).groupby("Property_type",as_index=False)['Price'].mean().sort_values(by='Price',ascending=False)[:10]
        fig = px.bar(df1,
                             title=' Property With MeanPrice ',
                             x="Property_type",
                             y="Price",
                             text="Price",
                             orientation='v',
                             color='Property_type',
                             color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True) 
        
        
        country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Price', 
                                       hover_data=['Price'],
                                       locationmode='country names',
                                       size='Price',
                                       title= 'MeanPrice In Each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True) 
        
    
