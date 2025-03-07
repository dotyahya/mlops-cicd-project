from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

# last test

class SentimentModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()
        self.model_path = 'models/sentiment_model.joblib'
        self.vectorizer_path = 'models/vectorizer.joblib'

    def train(self, X, y):
        # Transform the text data into TF-IDF features
        X_tfidf = self.vectorizer.fit_transform(X)
        
        # Train the classifier
        self.classifier.fit(X_tfidf, y)
        
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save the model and vectorizer
        joblib.dump(self.classifier, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)

    def predict(self, text):
        # Load the model and vectorizer if they exist
        if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
            self.classifier = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
        
        # Transform the text using the vectorizer
        X_tfidf = self.vectorizer.transform([text])
        
        # Make prediction
        prediction = self.classifier.predict(X_tfidf)
        return prediction[0] 