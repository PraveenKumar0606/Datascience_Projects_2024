from googleapiclient.discovery import build
import pymongo
import pymysql
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image



# SETTING PAGE CONFIGURATIONS
icon = Image.open("c:/Users/Praveen/Youtube_logo.png")
st.set_page_config(page_title= "Youtube Data Harvesting and Warehousing | By Praveen Kumar",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded")

#Creating option menu
with st.sidebar:
    selected = option_menu(None, ["Home","Collect and Store Data","Migrate to sql","View"], 
                           icons=["house-door-fill","card-text","database"],
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#33A5FF"},
                                   "icon": {"font-size": "30px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#33A5FF"}}) 

#API key Connection

def Api_connect():
    Api_id = "AIzaSyA7OS_aG6eMjgVCXrvoIwO62hgcnxBhO3E"
    
    api_service_name = "youtube"
    api_version="v3"
    
    youtube=build(api_service_name,api_version,developerKey=Api_id)
    
    return youtube 

youtube=Api_connect()
    
    
    
#gets channels information
def get_Channel_info(channel_id):
    request=youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id      
    )
    response=request.execute()

    for i in response['items']:
        data=dict(Channel_Name = i["snippet"]["title"],
                Channel_Id=i["id"],
                Subscribers=i['statistics']['subscriberCount'],
                Views=i["statistics"]["viewCount"],
                Total_videos=i["statistics"]["videoCount"],
                Channel_Description=i["snippet"]["description"],
                Playlist_Id=i["contentDetails"]["relatedPlaylists"]["uploads"])
    return data

#get video ids
def get_videos_ids(channel_id):
    video_ids =[]
    response=youtube.channels().list(id=channel_id,
                                    part='contentDetails').execute()
    Playlist_Id=response['items'][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    next_page_token=None

    while True:
        response1=youtube.playlistItems().list(
                                            part='snippet',
                                            playlistId=Playlist_Id,
                                            maxResults=50,
                                            pageToken=next_page_token).execute()
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token=response1.get('nextPageToken')
        
        if next_page_token is None:
            break    
    return video_ids   


#get Video information
def get_video_info(video_ids):
    video_data=[]
    for video_id in video_ids:
        request=youtube.videos().list(
            part='snippet,ContentDetails,statistics',
            id=video_id
        )
        response=request.execute()
        
        for item in response['items']:
            data=dict(Channel_Name=item['snippet']['channelTitle'],
                    Channel_Id=item['snippet']['channelId'],
                    Video_Id=item['id'],
                    Title=item['snippet']['title'],
                    Description=item['snippet'].get('description'),
                    Published_Date=item['snippet']['publishedAt'],
                    Duration=item['contentDetails']['duration'],
                    Views=item['statistics']['viewCount'],
                    Likes=item['statistics'].get('likeCount'),
                    Comments=item['statistics'].get('commentCount'),
                    Favorite_Count=item['statistics']['favoriteCount'],
                    Definition=item['contentDetails']['definition'],
                    caption_Status=item['contentDetails']['caption']
                    )
            video_data.append(data)
    return video_data    


#get comment information
def get_comment_info(video_ids):
    Comment_Information=[]
    try:
        for video_id in video_ids:
            request=youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=50
            )
            response=request.execute()
            
            for item in response['items']:
                data=dict(Comment_Id=item['snippet']['topLevelComment']['id'],
                        Video_Id = item["snippet"]["videoId"],
                        Comment_Text = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                        Comment_Author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                        Comment_Published = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"])
                
                Comment_Information.append(data)
    except:
        pass            
    return Comment_Information
        
             
 #upload to MongoDb
client=pymongo.MongoClient("mongodb://localhost:27017")
db=client["Youtube_data"]
my_coll=db.channel_details


def channel_details(channel_id):
    ch_details = get_Channel_info(channel_id)
    vi_ids = get_videos_ids(channel_id)
    vi_details = get_video_info(vi_ids)
    com_details = get_comment_info(vi_ids)

    coll1 = db["channel_details"]
    coll1.insert_one({"channel_information":ch_details,"video_information":vi_details,
                     "comment_information":com_details})
    
    return "upload completed successfully"


#Table Creation
def Channels_Table():
    mydb=pymysql.connect(host="127.0.0.1",
                    user="root",
                    password="12345",
                    database="Youtube_data",
                    port=3306)
    cursor=mydb.cursor()


    try:
        create_query='''create table if not exists channels(Channel_Name  varchar(100),
                                                            Channel_Id  varchar(80) primary key,
                                                            Subscribers varchar(100),
                                                            Views varchar(50),
                                                            Total_Videos varchar(100),
                                                            Channel_Description text)'''
        cursor.execute(create_query)
        mydb.commit()
    except:
        print("Channels Table already exists")  
        

    ch_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
        ch_list.append(ch_data["channel_information"])
    df=pd.DataFrame(ch_list)  
    
    
    
    for index,row in df.iterrows():
        insert_query = '''insert into channels(Channel_Name,
                                                Channel_Id,
                                                Subscribers,
                                                Views,
                                                Total_Videos,
                                                Channel_Description)
                                                
                                            values(%s,%s,%s,%s,%s,%s)'''
        values=(row['Channel_Name'],
                row['Channel_Id'],
                row['Subscribers'],
                row['Views'],
                row['Total_videos'],
                row['Channel_Description'])
        try:                     
                cursor.execute(insert_query,values)
                mydb.commit()    
        except:
            print("Channels values are already inserted")
    
                                                      

#Video table
def videos_table():
    mydb=pymysql.connect(host="127.0.0.1",
                    user="root",
                    password="12345",
                    database="youtube_data",
                    port=3306)
    cursor=mydb.cursor()


    create_query='''create table if not exists videos(Channel_Name varchar(100),
                                                    Channel_Id varchar(100),
                                                    Video_Id varchar(50),
                                                    Title varchar(150),
                                                    Description text,
                                                    Published_Date varchar(100),
                                                    Duration varchar(100),
                                                    Views int,
                                                    Likes int,
                                                    Comments int,
                                                    Favorite_Count int,
                                                    Definition varchar(10),
                                                    caption_Status varchar(20)
                                                    )'''
                                                  
    cursor.execute(create_query)
    mydb.commit()

        
    vi_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for vi_data in coll1.find({},{"_id":0,"video_information":1}):
        for i in range(len(vi_data["video_information"])):
          vi_list.append(vi_data["video_information"][i])
    df1=pd.DataFrame(vi_list)


    for index, row in df1.iterrows():
            insert_query = '''insert into videos(Channel_Name,
                            Channel_Id,
                            Video_Id, 
                            Title, 
                            Description, 
                            Published_Date,
                            Duration, 
                            Views, 
                            Likes,
                            Comments,
                            Favorite_Count, 
                            Definition, 
                            caption_Status 
                            )
                            
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                        
            values = ( row['Channel_Name'],
                       row['Channel_Id'],
                       row['Video_Id'],
                       row['Title'],
                       row['Description'],
                       row['Published_Date'],
                       row['Duration'],
                       row['Views'],
                       row['Likes'],
                       row['Comments'],
                       row['Favorite_Count'],
                       row['Definition'],
                       row['caption_Status']
                        )
                                    
            cursor.execute(insert_query,values)
            mydb.commit()
                                        

 #Comment table
def comments_table():
    mydb=pymysql.connect(host="127.0.0.1",
                  user="root",
                  password="12345",
                  database="youtube_data",
                  port=3306)
    cursor=mydb.cursor()



    create_query='''create table if not exists comments(Comment_Id varchar(100),
                                                      Video_Id varchar(50),
                                                      Comment_Text text,
                                                      Comment_Author varchar(150),
                                                      Comment_Published varchar(100)
                                                       )'''                                                     
    cursor.execute(create_query)
    mydb.commit()


    com_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for com_data in coll1.find({},{"_id":0,"comment_information":1}):
        for i in range(len(com_data["comment_information"])):
            com_list.append(com_data["comment_information"][i])
    df2=pd.DataFrame(com_list) 


    for index,row in df2.iterrows():
            insert_query = '''insert into comments(Comment_Id,
                                                    Video_Id,
                                                    Comment_Text,
                                                    Comment_Author,
                                                    Comment_Published 
                                                    )
                                                    
                                                values(%s,%s,%s,%s,%s)'''
            
            values=(row['Comment_Id'],
                    row['Video_Id'],
                    row['Comment_Text'],
                    row['Comment_Author'],
                    row['Comment_Published']
                    )
                                
            cursor.execute(insert_query,values)
            mydb.commit()    



def tables():
    Channels_Table()
    videos_table()
    comments_table()
    
    return "Tables Created Succesfully"


def show_channel_table():
    ch_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
        ch_list.append(ch_data["channel_information"])
    df=st.dataframe(ch_list)  
    
    return df


def show_videos_table():
    vi_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for vi_data in coll1.find({},{"_id":0,"video_information":1}):
        for i in range(len(vi_data["video_information"])):
            vi_list.append(vi_data["video_information"][i])
    df1=st.dataframe(vi_list) 
    
    return df1


def show_comments_table():
    com_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for com_data in coll1.find({},{"_id":0,"comment_information":1}):
        for i in range(len(com_data["comment_information"])):
           com_list.append(com_data["comment_information"][i])
    df2=st.dataframe(com_list) 
    
    
    return df2

#Streamlit 

#Home page
if selected=="Home":
    st.title(":rainbow[YOUTUBE DATA HARVESTING & WAREHOUSING]") 
    styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "0px" 
                                                }},
    

#collect and transform data
if selected=="Collect and Store Data":
    channel_id=st.text_input(" :blue[Enter the Channel ID]")
    st.write("## :green[Collecting and Storing Data into MongoDb]")
    if  st.button("Collect and Store Data"):
        ch_ids=[]    
        db=client["Youtube_data"]
        coll1=db["channel_details"]
        for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
            ch_ids.append(ch_data["channel_information"]["Channel_Id"])
                
        if channel_id in ch_ids:
           st.success("The Given Channel Ids already exists")
                
        else:
                insert=channel_details(channel_id)
                st.success(insert)    
                
                
#Migrate to sql
if selected=="Migrate to sql":
    st.write("## :red[Migrating from MongoDb to SQL]")
    if st.button("Migrate to SQL"):
        with st.spinner('Please Wait for it...'):
         Table=tables()
         st.success(Table)

    show_table=st.selectbox("choose",["CHANNELS","VIDEOS","COMMENTS"])

    if show_table=="CHANNELS":
        show_channel_table()
        
    elif show_table=="VIDEOS":
        show_videos_table()
        
    elif show_table=="COMMENTS":
        show_comments_table()
                                                          
#SQL  CONNECTION
mydb=pymysql.connect(host="127.0.0.1",
                user="root",
                password="12345",
                database="youtube_data",
                port=3306)
cursor=mydb.cursor()

# VIEW PAGE
if selected == "View":
    st.write("## :orange[Select any question to get Insights]")
    Question=st.selectbox("Select your Question",("1. What are the names of all the videos and their corresponding channels?",
            "2. Which channels have the most number of videos, and how many videos do they have?",
            "3. What are the top 10 most viewed videos and their respective channels?",
            "4. How many comments were made on each video, and what are their corresponding video names?",
            "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
            "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
            "7. What is the total number of views for each channel, and what are their corresponding channel names?",
            "8. What are the names of all the channels that have published videos in the year 2022?",
            "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
            "10. Which videos have the highest number of comments, and what are their corresponding channel names?"))                                                                            
                                                        
    if Question=="1. What are the names of all the videos and their corresponding channels?":
        query1='''select title as videos,channel_name as channelname from videos'''
        cursor.execute(query1)
        mydb.commit()
        t1=cursor.fetchall()
        df=pd.DataFrame(t1,columns=["video_title","channel name"])
        st.write(df)                                                   
                                                        
    elif Question=="2. Which channels have the most number of videos, and how many videos do they have?":
        query2='''select channel_name as channelname,total_videos as no_videos from channels
                order by total_videos desc'''
        cursor.execute(query2)
        mydb.commit()
        t2=cursor.fetchall()
        df2=pd.DataFrame(t2,columns=["channel_name","No of videos"])
        st.write(df2)  

    elif Question=="3. What are the top 10 most viewed videos and their respective channels?":
        query3='''select views as views,channel_name as channelname,title as videotitle from videos
                where views is not null order by views desc limit 10'''
        cursor.execute(query3)
        mydb.commit()
        t3=cursor.fetchall()
        df3=pd.DataFrame(t3,columns=["views","channel name","videotitle"])
        st.write(df3)  
            
    elif Question=="4. How many comments were made on each video, and what are their corresponding video names?":
        query4='''select comments as no_comments,title as videotitle from videos where comments is not null'''
        cursor.execute(query4)
        mydb.commit()
        t4=cursor.fetchall()
        df4=pd.DataFrame(t4,columns=["no of comments","videotitle"])
        st.write(df4)  

    elif Question=="5. Which videos have the highest number of likes, and what are their corresponding channel names?":
        query5='''select title as videotitle,channel_name as channelname,Likes as likecount
                from videos where Likes is not null order by Likes desc'''
        cursor.execute(query5)
        mydb.commit()
        t5=cursor.fetchall()
        df5=pd.DataFrame(t5,columns=["videotitle","channelname","likecount"])
        st.write(df5)  

    elif Question=="6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
        query6='''select likes as likecount,title as videotitle from videos'''
        cursor.execute(query6)
        mydb.commit()
        t6=cursor.fetchall()
        df6=pd.DataFrame(t6,columns=["likecount","videotitle"])
        st.write(df6)  

    elif Question=="7. What is the total number of views for each channel, and what are their corresponding channel names?":
        query7='''select channel_name as channelname,views as Totalviews from channels'''
        cursor.execute(query7)
        mydb.commit()
        t7=cursor.fetchall()
        df7=pd.DataFrame(t7,columns=["channel name","Total views"])
        st.write(df7)  


    elif Question=="8. What are the names of all the channels that have published videos in the year 2022?":
        query8='''select title as video_title,published_date as videorelease,channel_name as channelname from videos
                where extract(year from published_date)=2022'''
        cursor.execute(query8)
        mydb.commit()
        t8=cursor.fetchall()
        df8=pd.DataFrame(t8,columns=["videotitle","published_date","channelname"])
        st.write(df8)  


    elif Question=="9. What is the average duration of all videos in each channel, and what are their corresponding channel names?":
        query9='''select channel_name as channelname,AVG(duration) as averageduration from videos 
                group by channel_name'''
        cursor.execute(query9)
        mydb.commit()
        t9=cursor.fetchall()
        df9=pd.DataFrame(t9,columns=["channel name","averageduration"])
        st.write(df9)  
        
        T9=[]
        for index,row in df9.iterrows():
            channel_title=row["channel name"]
            average_duration=row["averageduration"]
            average_duration_str=str(average_duration)
            T9.append(dict(channeltitle=channel_title,avgduration=average_duration_str))
        df1=pd.DataFrame(T9)
        st.write(df1)
        
    elif Question=="10. Which videos have the highest number of comments, and what are their corresponding channel names?":
        query10='''select title as videotitle, channel_name as channelname, Comments as comments from videos
                where Comments is not null order by comments desc'''
        cursor.execute(query10)
        mydb.commit()
        t10=cursor.fetchall()
        df10=pd.DataFrame(t10,columns=["video title","channel name","comments"])
        st.write(df10)  
                                                                                 
                                                      
