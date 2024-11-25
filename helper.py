from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user'] == selected_user]

    # fetching the number of messages
    num_messages= df.shape[0]

    # fetching the number of words
    words = []
    for m in df['message']:
        words.extend(m.split())

    # fetching the no of rows emitted media
    media=df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetching the number of links shared
    links=[]
    for m in df['message']:
        links.extend(extract.find_urls(m))
    return num_messages, len(words) , media , len(links)


def fetch_most_users(df):
    x=df['user'].value_counts().head()

    ddf=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percentage'})
    return x,ddf


def create_word_cloud(selected_user,df):
        f = open('stop_hinglish.txt', 'r')
        stop_words = f.read().splitlines()  # Split into a list of stop words
        f.close()

        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        # Filter out unwanted messages
        temp = df[(df['message'] != 'group_notification') &
              (df['message'].str.strip() != '<Media omitted>')]
        def remove_stop_words(message):
            y=[]
            for word in message.lower().split():
                if word not in stop_words:
                    y.append(word)
            return ' '.join(y)

        wc=WordCloud(width=500,height=500, min_font_size=10, background_color='white')
        temp['message']=temp['message'].apply(remove_stop_words)
        df_wc=wc.generate(temp['message'].str.cat(sep=" "))
        return df_wc


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read().splitlines()  # Split into a list of stop words
    f.close()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out unwanted messages
    temp = df[(df['message'] != 'group_notification') &
              (df['message'].str.strip() != '<Media omitted>')]

    words = []
    for m in temp['message']:
        for word in m.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

def emoji_helper(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for m in df['message']:
        emojis.extend([c for c in m if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline

def days_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity_mpp=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_mpp


