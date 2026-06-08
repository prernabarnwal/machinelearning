import re
import pandas as pd

def preprocess(data):
    #pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    #messages = re.split(pattern, data)[1:]
    #dates = re.findall(pattern, data)
    #df = pd.DataFrame({'user_message': messages, 'date': dates})
    # converting to date_time format
    #df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M - ')

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:am|pm\s)-\s'
    messages = re.split(pattern, data)[1:]
    type(messages)
    msg = []
    for i in range(len(messages)):
        # print(messages[i])
        if (messages[i] != 'am' and messages[i] != 'pm'):
            msg.append(messages[i])
    data = data.replace('\u202f', ' ').replace('\u00A0', ' ')
    matches = re.finditer(pattern, data)
    dates = []
    for m in matches:
        dates.append(m.group())
    df = pd.DataFrame({'user_message': messages, 'date': dates})
    # converting to date_time format
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M %p - ')














    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['days'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['days', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df