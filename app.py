import streamlit as st
import pandas as pd
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

        if df.empty:
            st.error("No valid data found in the file!")
        else:
            # Fetch unique users
            user_list = df['user'].unique().tolist()
            user_list.sort()
            user_list.insert(0, "Overall")

            selected_user = st.sidebar.selectbox("Analyze messages from:", user_list)

            if st.sidebar.button("Show Analysis"):
                st.title("Chat Analysis")

                # Fetch statistics
                num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)

                st.subheader("Top Statistics")
                st.write(f"Total Messages: {num_messages}")
                st.write(f"Total Words: {num_words}")
                st.write(f"Total Media Shared: {num_media}")
                st.write(f"Total Links Shared: {num_links}")

                # Monthly timeline
                st.subheader("Monthly Timeline")
                monthly_df = helper.monthly_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(monthly_df['month'], monthly_df['message_count'], marker='o', color='b')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                # Most Busy Day
                st.subheader("Most Busy Day")
                busy_day = helper.most_busy_day(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                # Most Busy Month
                st.subheader("Most Busy Month")
                busy_month = helper.most_busy_month(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                # Activity heatmap
                st.subheader("Activity Heatmap")
                heatmap_data = helper.activity_heatmap(selected_user, df)
                st.pyplot(heatmap_data)

                # WordCloud
                st.subheader("Word Cloud")
                wordcloud = helper.create_wordcloud(selected_user, df)
                fig, ax = plt.subplots()
                ax.imshow(wordcloud)
                plt.axis("off")
                st.pyplot(fig)

                # Most common words
                st.subheader("Most Common Words")
                common_words_df = helper.most_common_words(selected_user, df)
                st.dataframe(common_words_df)

                # Emoji Analysis
                st.subheader("Emoji Analysis")
                emoji_df = helper.emoji_analysis(selected_user, df)

                if not emoji_df.empty:
                    st.dataframe(emoji_df)

                    # Plot emoji frequency
                    fig, ax = plt.subplots()
                    ax.bar(emoji_df['Emoji'], emoji_df['Frequency'], color='orange')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                else:
                    st.write("No emojis found in the chat.")

                # Most active users
                if selected_user == "Overall":
                    st.subheader("Most Active Users")
                    active_users_df, active_users_chart = helper.most_active_users(df)
                    st.dataframe(active_users_df)
                    st.pyplot(active_users_chart)
    except Exception as e:
        st.error(f"Error parsing file: {str(e)}")