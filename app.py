import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Wap Chat Analyzer")
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    #st.dataframe(df)  #to display the dataframe

    user_list= df['user'].unique().tolist() #fetch unique users
    user_list.remove('notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user= st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Analyze"):
        num_msgs, words, num_media_msg= helper.fetch_stats(selected_user,df)
        st.title("Message Analyzer")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Total messages")
            st.title(num_msgs)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Total media messages")
            st.title(num_media_msg)

        #timeline

        st.title("Monthly Timeline")
        timeline, busy_month=helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(7,4))
        ax.plot(timeline['time'], timeline['message'],color='brown')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.title("Activity Map")
        col1, col2 = st.columns(2)
        daily_timeline, busy_day = helper.daily_timeline(selected_user, df)
        with col1:
            st.header("Most Busy Day")
            fig, ax = plt.subplots(figsize=(7,4))
            ax.bar(daily_timeline['days'], daily_timeline['message'],color='purple')
            plt.xticks(rotation=90)
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            fig, ax = plt.subplots(figsize=(7,4))
            ax.bar(timeline['month'], timeline['message'], color='blue')
            plt.xticks(rotation=90)
            st.pyplot(fig)
            #ax.bar(busy_month.index, busy_month.values, color='red')
            #plt.xticks(rotation=90)
            #st.pyplot(fig)
        st.title("Activity Heatmap")
        pivot_table = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(pivot_table, cmap="rocket")
        st.pyplot(fig)



        #finding the busiest users in the group(Group level)
        if selected_user=="Overall":
            st.title("Most busy users")
            x, new_df=helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='pink')
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #wordcloud
        st.title("word cloud")
        df_wc= helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_common_df=helper.most_common_words(selected_user,df)

        st.title("Frequently used words")
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0],most_common_df[1], color='yellow')
            plt.xticks(rotation=90)
            st.pyplot(fig)
        with col2:
            st.dataframe(most_common_df, width=300)

        #emoji analysis
        st.title("Emoji analysis")
        emoji_df = helper.emoji_finder(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df, width=300)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct='%0.2f%%')
            st.pyplot(fig)

