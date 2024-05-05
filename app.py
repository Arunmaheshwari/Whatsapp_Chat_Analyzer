import streamlit as st
import preprocessor, helpher
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    # fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to: ",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area

        num_messages, words, num_media_messages, num_links = helpher.fetch_stats(selected_user, df)

        st.header("Top Statistics",divider='rainbow')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("<h3 style='font-size: 24px;'>Total Messages</h3>", unsafe_allow_html=True)

            st.title(num_messages)

        with col2:
            st.markdown("<h3 style='font-size: 24px;'>Total Words</h3>", unsafe_allow_html=True)

            st.title(words)

        with col3:
            #st.header("Media Shared",divider='rainbow')
            st.markdown("<h3 style='font-size: 24px;'>Media Shared</h3>", unsafe_allow_html=True)
            st.title(num_media_messages)

        with col4:
            #st.header("Links Shared",divider='rainbow')
            st.markdown("<h3 style='font-size: 24px;'>Links Shared</h3>", unsafe_allow_html=True)
            st.title(num_links)

        # Monthly timeline
        st.header("Monthly Timeline", divider='rainbow')
        timeline = helpher.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'],color = 'purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.header("Daily Timeline", divider='rainbow')
        daily_timeline = helpher.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='yellow')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.header('Activity Map', divider='rainbow')
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h3 style='font-size: 28px;'>Most busy days</h3>", unsafe_allow_html=True)
            busy_day = helpher.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("<h3 style='font-size: 28px;'>Most busy months</h3>", unsafe_allow_html=True)
            busy_month = helpher.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        # Weekly activity map
        st.header("Weekly activity map", divider='rainbow')
        user_heatmap = helpher.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.header("Most Busy User",divider='rainbow')
            x,new_df = helpher.most_busy_users(df)
            fig, ax = plt.subplots()

            col1 ,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='yellow')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)



        # Most common word
        most_common_df = helpher.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1], color='pink')
        plt.xticks(rotation = 'vertical')
        st.header("Most Common Word", divider='rainbow')
        st.pyplot(fig)

        # Emoji analysis
        emoji_df = helpher.emoji_helper(selected_user, df)
        st.header("Emoji Analysis", divider='rainbow')

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()

            ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(), autopct = '%0.2f')
            st.pyplot(fig)

        # Display Frequent Words WordCloud
        st.header("Frequent Words", divider='rainbow')
        df_wc = helpher.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Read the content of the footer HTML file
        with open("footer.html", "r") as file:
            footer_html = file.read()

            # Render the footer HTML
        st.markdown(footer_html, unsafe_allow_html=True)
