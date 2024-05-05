import re
import pandas as pd
from datetime import datetime
from dateutil import parser



def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[AP]M\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [string.replace('d', " ") for string in dates]

    # Define a function to convert 12-hour time format to 24-hour time format
    def convert_to_24_hour(time_str):
        # Remove the trailing space and hyphen
        time_str = time_str.rstrip(' -')
        # Parse the time string into a datetime object


        # Parse a date and time string
        #dt_obj = parser.parse(time_str, '%m/%d/%y, %I:%M %p')
        dt_obj = datetime.strptime(time_str, '%m/%d/%y, %I:%M %p')
        # Format the datetime object to 24-hour time format
        return dt_obj.strftime('%m/%d/%y, %H:%M - ')

    # Convert each time string in the list to 24-hour format
    new_dates = [convert_to_24_hour(time_str) for time_str in dates]

    df = pd.DataFrame({'user_message': messages, 'message_date': new_dates})
    # Convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df