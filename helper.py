from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    num_media_msg=df[df['message'] == '<Media omitted>\n'].shape[0]
    return num_messages, len(words), num_media_msg

def most_busy_users(df):
    x= df['user'].value_counts().head()
    df=round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    wc= WordCloud(background_color='white', width=300, height=200, min_font_size=10)
    df_wc= wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for msg in temp['message']:
        words.extend(msg.split())
    df_final= pd.DataFrame(Counter(words).most_common(20))
    return df_final

def emoji_finder(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
    emoji_df= pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline, df['month'].value_counts()

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby(['days']).count()['message'].reset_index()
    return daily_timeline, df['days'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    pivot_table= df.pivot_table(index='days',columns='period',values='message', aggfunc='count').fillna(0)
    return pivot_table