import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize NLTK
nltk.download('punkt', quiet=True)
print("NLTK 'punkt' tokenizer downloaded.")
nltk.download('stopwords', quiet=True)
print("NLTK 'stopwords' downloaded.")
nltk.download('punkt_tab')
print("NLTK 'punkt_tab' downloaded.")
nltk.download("wordnet", quiet=True)
print("NLTK 'wordnet' downloaded.")
nltk.download("omw-1.4", quiet=True)
print("NLTK 'omw-1.4' downloaded.")


STOP_WORDS = set(stopwords.words('english'))

lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    
    cleaned = []

    for word in tokens:
        if word not in STOP_WORDS:
            word = (
                lemmatizer
                .lemmatize(word)
            )
            cleaned.append(word)

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

            if scores[idx] <= 0:
                continue

            results.append({
            "name": self.df.iloc[idx]["Movie Name"],
            "plot": self.df.iloc[idx]["Storyline"],
            "score": float(scores[idx])
            })

            if len(results) == top_n:
                break

        return results