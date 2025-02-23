import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from nltk.corpus import stopwords
import nltk
import emoji
import re

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
    "fir", "phir", "ki", "ke", "yeh", "vo", "koi", "isse", "usse", "jise", "jaise"
}

# ✅ Merging Marathi and Hindi stopwords
custom_stopwords = marathi_stopwords.union(hindi_stopwords)

# ✅ Function to remove emojis from text
def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # Transport & map symbols
        u"\U0001F700-\U0001F77F"  # Alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric shapes
        u"\U0001F800-\U0001F8FF"  # Supplemental arrows
        u"\U0001F900-\U0001F9FF"  # Supplemental symbols and pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess symbols, legacy computing
        u"\U0001FA70-\U0001FAFF"  # Symbols and pictographs extended
        u"\U00002702-\U000027B0"  # Dingbats
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)  # Replace emojis with an empty string

# ✅ Function to create the word cloud (Now removes emojis)
def create_wordcloud(selected_user, df):
    stop_words = set(stopwords.words('english')).union(custom_stopwords)  # ✅ Combine Marathi, Hindi & English stopwords

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Filter out media messages
    filtered_messages = df[~df['message'].str.contains("Media omitted|omitted media", case=False, na=False, regex=True)]['message']

    # Remove emojis before generating the Word Cloud
    text = " ".join(filtered_messages)
    text = remove_emojis(text)  # ✅ Apply emoji removal function

    # Generate Word Cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, stopwords=stop_words, background_color='black').generate(text)

    return wc

# ✅ Function to analyze emoji usage (unchanged)
def emoji_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_counter = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counter.most_common(len(emoji_counter)), columns=["Emoji", "Frequency"])

    return emoji_df
