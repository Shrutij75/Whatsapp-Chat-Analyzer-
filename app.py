import streamlit as st
import pandas as pd
import preprocessor,helper
import seaborn as sns

import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # Read uploaded file
    bytes_data = uploaded_file.getvalue()
    try:
        data = bytes_data.decode("utf-8")
        # st.text("Uploaded File Preview (First 500 characters):")
        # st.text(data[:500])  # Show a preview of the uploaded data
    except UnicodeDecodeError:
        st.error("Unable to decode the uploaded file. Please ensure it is UTF-8 encoded.")

    # Process data
    try:
        df = preprocessor.preprocess(data)
        if df.empty:
            st.warning("The data could not be parsed. Ensure the chat file matches the expected format.")
        else:
            # st.success("Data processed successfully!")
            # st.dataframe(df)

            # fetch unique users
            user_list = df['user'].unique().tolist()
            user_list.remove('group_notification')
            user_list.sort()
            user_list.insert(0,"Overall")
            selected_user=st.sidebar.selectbox("Show Analysis wrt", user_list)

            if st.sidebar.button("Show Analysis"):
                num_messages,words,media,links =helper.fetch_stats(selected_user,df)
                st.title("TOP STATISTICS")
                col1 , col2 , col3, col4 = st.columns(4)
                with col1:
                    st.header("Total Messages")
                    st.title(num_messages)
                with col2:
                    st.header("Total Words")
                    st.title(words)
                with col3:
                    st.header("Media Shared")
                    st.title(media)
                with col4:
                    st.header("Links Shared")
                    st.title(links)

                # monthly timeline
                st.title(" MONTHLY TIMELINE")
                timeline=helper.monthly_timeline(selected_user,df)
                fig , ax=plt.subplots()
                ax.plot(timeline['time'],timeline['message'],color='green')
                plt.xticks(rotation=90)
                st.pyplot(fig)

                # daily timeline
                st.title(" DAILY TIMELINE")
                d_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(d_timeline['only_date'], d_timeline['message'], color='blue')
                plt.xticks(rotation=90)
                st.pyplot(fig)

                # day wise activity map of the user
                st.title('Activity Map')
                col1,col2=st.columns(2)
                with col1:
                    st.header("Most Busy Day")
                    busy_day=helper.days_activity_map(selected_user,df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_day.index,busy_day.values,color='yellow')
                    plt.xticks(rotation=90)
                    st.pyplot(fig)
                with col2:
                    st.header("Most Busy Month")
                    busy_month=helper.month_activity_map(selected_user,df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_month.index,busy_month.values,color='green')
                    plt.xticks(rotation=90)
                    st.pyplot(fig)

                # heatmap
                st.title("WEEKLY ACTIVITY MAP")
                user_heatmap=helper.activity_map(selected_user,df)
                fig,ax =plt.subplots()
                ax=sns.heatmap(user_heatmap)
                st.pyplot(fig)


                # fetching the top5 users who do max. chat in the group
                if selected_user == "Overall":
                    st.title("Most Busy Users")
                    x,new_df=helper.fetch_most_users(df)
                    fig , ax=plt.subplots()
                    col1 , col2=st.columns(2)
                    with col1:
                        ax.bar(x.index,x.values,color='r')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    with col2:
                        st.dataframe(new_df)

                #wordcloud -->>the most used words during the chat
                st.title("WORD-CLOUD")
                df_wc=helper.create_word_cloud(selected_user,df)
                fig, ax=plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)

            #most common words
            most_common= helper.most_common_words(selected_user,df)
            fig , ax = plt.subplots()
            st.title("Most Common Words")
            ax.barh(most_common[0],most_common[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            #most common emojis
            common_emoji = helper.emoji_helper(selected_user, df)
            st.title("Common Emoji")

            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(common_emoji)
            with col2:
                # Ensure numeric data for pie chart
                frequencies = pd.to_numeric(common_emoji[1].head(), errors='coerce')
                labels = common_emoji[0].head()

                fig, ax = plt.subplots()
                ax.pie(
                    frequencies,
                    labels=labels,
                    autopct="%0.2f%%"
                )
                st.pyplot(fig)


    except Exception as e:
        st.error(f"An error occurred during preprocessing: {e}")
else:
    st.info("Please upload a WhatsApp chat file to proceed.")


