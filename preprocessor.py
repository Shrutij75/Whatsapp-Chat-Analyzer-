import re
import pandas as pd


def preprocess(data):
    # Pattern for timestamps
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s[APap][Mm]))'

    try:
        # Extract messages and dates
        messages = re.split(pattern, data)[1:]
        messages = messages[1::2]
        dates = re.findall(pattern, data)

        # Check if splitting was successful
        if not messages or not dates or len(messages) != len(dates):
            print("Regex split did not align messages and dates.")
            print(f"Extracted {len(messages)} messages and {len(dates)} dates.")
            return pd.DataFrame()

        # Create DataFrame
        df = pd.DataFrame({'User_Messages': messages, 'Messages_Date': dates})

        # Convert `Messages_Date` to datetime
        df['Messages_Date'] = pd.to_datetime(df['Messages_Date'],
                                             format='%d/%m/%y, %I:%M %p',
                                             errors='coerce')
        if df['Messages_Date'].isnull().any():
            print("Some dates could not be parsed. Check the date format.")
            print(df[df['Messages_Date'].isnull()])

        df.rename(columns={'Messages_Date': 'date'}, inplace=True)

        # Extract users and messages
        users = []
        messages = []
        for message in df['User_Messages']:
            entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)  # Ensure maxsplit is set
            if len(entry) > 2:
                users.append(entry[1])
                messages.append(entry[2])
            else:
                users.append("group_notification")
                messages.append(entry[0])

        df['user'] = users
        df['message'] = messages

        # Drop the original message column
        df.drop(columns=['User_Messages'], inplace=True)

        # Extract additional time information
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['only_date'] = df['date'].dt.date
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        period = []
        for hour in df[['day_name', 'hour']]['hour']:
            if hour == 23:
                period.append(str(hour) + "-" + str('00'))
            elif hour == 0:
                period.append(str('00') + "-" + str(hour + 1))
            else:
                period.append(str(hour) + "-" + str(hour + 1))

        df['period'] = period

        return df

    except Exception as e:
        print(f"Error in preprocess: {e}")
        return pd.DataFrame()

# streamlit run app.py-->command to start the app

