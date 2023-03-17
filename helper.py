from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
import pandas as pd
from collections import Counter
extract=URLExtract()

def fetch_stats(selected_user,df):

    if selected_user!="Overall":
        df=df[df['user']==selected_user]


    # 1.fetch number of messages
    num_messages=df.shape[0]

    # 2.fetch number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())

    # 3.fetch number of media messsages
    num_media_messages = df[df["message"]=="<Media omitted>\n"].shape[0]
    
    # 4.fetch number of links shared
    links=[]
    for message in df["message"]:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)


def most_busy_users(df):
    x = df["user"].value_counts().head()
    y=round((df["user"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name' , 'user':'percent'})
    return x,y


def create_wordcloud(selected_user,df):
    if selected_user !="Overall":
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')

    # df_wc is basically a image ...'generate' function helps to generate the wordcloud as an image i.e..,generats from df["message"] column.......sep="space" seperates every word and put it on the image.
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    # reset_index is used to show the values in dataframe form
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    
    # merging year and month column
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time    
    
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    
    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    
    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    
    user_heatmap = df.pivot_table(index='day_name',columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

    

    