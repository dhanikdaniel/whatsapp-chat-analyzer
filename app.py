import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("UTF-8")
    df=preprocessor.preprocess(data)

    # showing dataframe of the chat
    # st.dataframe(df)

    # fetch unique users
    user_list=df["user"].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox('Show analysis wrt',user_list)

    if st.sidebar.button('Show Analysis'):
    
        num_messages,words,num_media_messages,num_links= helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total Words")
            st.title(words)      
        
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links shared")
            st.title(num_links)
        
        # Monthly timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        
        # plotting time and message
        ax.plot(timeline['time'],timeline['message'],color='green')
        
        # using xticks for rotating the x-values 
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # ------------------------------------------
        # Daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='violet')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # ------------------------------------------
        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)
        
        # for busy day(individaul and group level)
        with col1:
            st.header('Most busy day')
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # for busy month(individual and group level)
        with col2:
            st.header('Most busy month')
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

    # ----------------------------------------------- 
        # Creating heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)




        # finding the busiest users in the group(group level)
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x,new_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
        
        # word cloud
        st.title("Word Cloud")
        # below code gives us an image of the wordcloud
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        # using imshow() function to display the image
        ax.imshow(df_wc)
        st.pyplot(fig)


        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        # creating columns 
        if emoji_df.shape!=(0,0):
            emoji_df.rename(columns={0:'Emoji',1:'Count'},inplace=True)
            col1,col2=st.columns(2)
            with col1:
            # printing dataframe
                st.dataframe(emoji_df)
            with col2:
            # printing piechart
                fig,ax = plt.subplots()
            # passing two things in pie fuction i..e, we pass values in pie function and passing labels seperately 
            # autopct is used for showing percentage for the below pie chart
                ax.pie(emoji_df['Count'].head(),labels=emoji_df['Emoji'].head(),autopct="%0.2f")
                st.pyplot(fig)
        else:
            st.title('User haven\'t used any emoji')