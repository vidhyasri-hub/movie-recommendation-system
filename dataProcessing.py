import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize NLTK
nltk.download('punkt', quiet=True)
print("NLTK 'punkt' tokenizer downloaded.")
nltk.download('stopwords', quiet=True)
print("NLTK 'stopwords' downloaded.")
nltk.download('punkt_tab')
print("NLTK 'punkt_tab' downloaded.")

STOP_WORDS = set(stopwords.words('english'))

def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    return " ".join([w for w in tokens if w not in STOP_WORDS])

class RecommendationEngine:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df['cleaned_plot'] = self.df['Storyline'].apply(clean_text)
        self.vectorizer = TfidfVectorizer()
        self.matrix = self.vectorizer.fit_transform(self.df['cleaned_plot'])

    def get_recommendations(self, user_input, top_n=5):
        cleaned_input = clean_text(user_input)
        input_vector = self.vectorizer.transform([cleaned_input])
        scores = cosine_similarity(input_vector, self.matrix).flatten()
        
        top_indices = scores.argsort()[-top_n:][::-1]
        
        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                results.append({
                    "name": self.df.iloc[idx]['Movie Name'],
                    "plot": self.df.iloc[idx]['Storyline'],
                    "score": scores[idx]
                })
        return results