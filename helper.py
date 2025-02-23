import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from nltk.corpus import stopwords
import nltk
import emoji

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords')

# ✅ Custom list of Marathi stopwords (English script)
marathi_stopwords = {
    "ka", "ho", "zala", "pn", "ky", "la", "tr", "nhi", "na", "ok", "ata", "ch",
    "ahe", "ha", "ani", "mg", "hota", "tu", "nay", "kay", "mala", "te", "pan",
    "cha", "ki", "tya", "nahi", "to", "he", "mi", "majha", "tuzha", "amcha",
    "tumcha", "mag", "kahi", "karan", "tar", "ti", "tula", "br", "madhe", "mdhe"
}

# ✅ Common Hindi stopwords (English script)
hindi_stopwords = {
    "hai", "haan", "nahi", "kyu", "kyun", "ho", "gaya", "kya", "kaise", "kar", "raha",
    "rhe", "rhi", "kr", "tha", "thi", "hun", "bhi", "par", "pr", "ab", "aur", "se",
    "sab", "wo", "woh", "jo", "uska", "unka", "mera", "tera", "hamara", "inka",
    "unka", "kuch", "toh", "lekin", "magar", "sirf", "bus", "kyunki", "jab", "tab",
    "fir", "phir", "ki", "ke", "yeh", "vo", "koi", "isse", "usse", "jise", "jaise" , "🎂", "😂", "🥳", "💐", "🌞", "🙏", "🎊"
}

# ✅ Merging Marathi and Hindi stopwords
custom_stopwords = marathi_stopwords.union(hindi_stopwords)

# Function to fetch statistics
def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    num_words = df['message'].apply(lambda x: len(str(x).split())).sum()
    num_media = df[df['message'] == "<Media omitted>"].shape[0]
    num_links = df['message'].str.contains(r'http[s]?://', regex=True).sum()

    return num_messages, num_words, num_media, num_links

# Function to generate the monthly timeline
def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()
    timeline['month'] = timeline['month'].astype(str) + "-" + timeline['year'].astype(str)

    return timeline[['month', 'message']].rename(columns={'message': 'message_count'})

# Function to create the activity heatmap
def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    activity = df.pivot_table(index="day_name", columns="hour", values="message", aggfunc="count").fillna(0)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(activity, cmap="coolwarm", ax=ax)

    return fig

# Function to create the word cloud
def create_wordcloud(selected_user, df):
    stop_words = set(stopwords.words('english')).union(custom_stopwords)  # ✅ Combine Marathi, Hindi & English stopwords

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Filter out media messages
    filtered_messages = df[~df['message'].str.contains("Media omitted|omitted media", case=False, na=False, regex=True)]['message']

    # Generate WordCloud while removing stopwords
    text = " ".join(filtered_messages)
    wc = WordCloud(width=500, height=500, min_font_size=10, stopwords=stop_words, background_color='black').generate(text)

    return wc

# Function to get most common words
def most_common_words(selected_user, df):
    stop_words = set(stopwords.words('english')).union(custom_stopwords)  # ✅ Combine Marathi, Hindi & English stopwords

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    words = []
    for msg in df['message']:
        for word in msg.lower().split():
            if word not in stop_words and word.isalpha():
                words.append(word)

    common_words_df = pd.DataFrame(Counter(words).most_common(20), columns=["Word", "Frequency"])
    return common_words_df

# Function to find most active users
def most_active_users(df):
    user_counts = df['user'].value_counts().head()
    user_df = user_counts.reset_index().rename(columns={'index': 'User', 'user': 'Message Count'})

    fig, ax = plt.subplots()
    ax.bar(user_counts.index, user_counts.values, color='purple')
    plt.xticks(rotation='vertical')

    return user_df, fig

# Function to analyze emoji usage
def emoji_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_counter = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counter.most_common(len(emoji_counter)), columns=["Emoji", "Frequency"])

    return emoji_df

# Function to find most busy day
def most_busy_day(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    busy_day = df['day_name'].value_counts()
    return busy_day

# Function to find most busy month
def most_busy_month(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    busy_month = df['month'].value_counts()
    return busy_month
