"""
Interview Question Model Training Script
This script trains a machine learning model to:
1. Classify questions by category and difficulty
2. Generate relevant follow-up questions
3. Evaluate answer quality

Uses only free, local libraries (no API costs!)
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import json
from collections import defaultdict

class InterviewModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 3))
        self.difficulty_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.category_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.difficulty_encoder = LabelEncoder()
        self.category_encoder = LabelEncoder()
        self.questions_db = None
        
    def load_data(self, csv_path='interview_questions.csv'):
        """Load and preprocess the interview questions dataset"""
        print("📚 Loading dataset...")
        df = pd.read_csv(csv_path)
        print(f"✅ Loaded {len(df)} questions")
        print(f"   - Categories: {df['category'].unique()}")
        print(f"   - Roles: {df['role'].unique()}")
        print(f"   - Difficulty levels: {df['difficulty'].unique()}")
        
        self.questions_db = df
        return df
    
    def train(self, df):
        """Train the model on the dataset"""
        print("\n🔧 Training model...")
        
        # Prepare features
        X = self.vectorizer.fit_transform(df['question'])
        
        # Encode labels
        y_difficulty = self.difficulty_encoder.fit_transform(df['difficulty'])
        y_category = self.category_encoder.fit_transform(df['category'])
        
        # Split data
        X_train, X_test, y_diff_train, y_diff_test = train_test_split(
            X, y_difficulty, test_size=0.2, random_state=42
        )
        _, _, y_cat_train, y_cat_test = train_test_split(
            X, y_category, test_size=0.2, random_state=42
        )
        
        # Train classifiers
        print("   Training difficulty classifier...")
        self.difficulty_classifier.fit(X_train, y_diff_train)
        diff_score = self.difficulty_classifier.score(X_test, y_diff_test)
        
        print("   Training category classifier...")
        self.category_classifier.fit(X_train, y_cat_train)
        cat_score = self.category_classifier.score(X_test, y_cat_test)
        
        print(f"\n✅ Model trained successfully!")
        print(f"   - Difficulty prediction accuracy: {diff_score*100:.2f}%")
        print(f"   - Category prediction accuracy: {cat_score*100:.2f}%")
        
    def save_model(self, path='model'):
        """Save the trained model"""
        print(f"\n💾 Saving model to {path}/...")
        
        import os
        os.makedirs(path, exist_ok=True)
        
        # Save model components
        with open(f'{path}/vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)
        with open(f'{path}/difficulty_classifier.pkl', 'wb') as f:
            pickle.dump(self.difficulty_classifier, f)
        with open(f'{path}/category_classifier.pkl', 'wb') as f:
            pickle.dump(self.category_classifier, f)
        with open(f'{path}/difficulty_encoder.pkl', 'wb') as f:
            pickle.dump(self.difficulty_encoder, f)
        with open(f'{path}/category_encoder.pkl', 'wb') as f:
            pickle.dump(self.category_encoder, f)
        
        # Save questions database
        self.questions_db.to_csv(f'{path}/questions_db.csv', index=False)
        
        print("✅ Model saved successfully!")
        
    def load_model(self, path='model'):
        """Load a trained model"""
        print(f"📂 Loading model from {path}/...")
        
        with open(f'{path}/vectorizer.pkl', 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open(f'{path}/difficulty_classifier.pkl', 'rb') as f:
            self.difficulty_classifier = pickle.load(f)
        with open(f'{path}/category_classifier.pkl', 'rb') as f:
            self.category_classifier = pickle.load(f)
        with open(f'{path}/difficulty_encoder.pkl', 'rb') as f:
            self.difficulty_encoder = pickle.load(f)
        with open(f'{path}/category_encoder.pkl', 'rb') as f:
            self.category_encoder = pickle.load(f)
        
        self.questions_db = pd.read_csv(f'{path}/questions_db.csv')
        
        print("✅ Model loaded successfully!")
        
    def get_questions(self, role='Software Engineer', category='Technical', 
                     difficulty=None, num_questions=5):
        """Get interview questions based on criteria"""
        df = self.questions_db
        
        # Filter by role and category
        filtered = df[(df['role'] == role) & (df['category'] == category)]
        
        # Filter by difficulty if specified
        if difficulty:
            filtered = filtered[filtered['difficulty'] == difficulty]
        
        # Sample random questions
        if len(filtered) > num_questions:
            questions = filtered.sample(n=num_questions)
        else:
            questions = filtered
            
        return questions['question'].tolist()
    
    def predict_difficulty(self, question):
        """Predict the difficulty of a question"""
        X = self.vectorizer.transform([question])
        pred = self.difficulty_classifier.predict(X)[0]
        return self.difficulty_encoder.inverse_transform([pred])[0]
    
    def predict_category(self, question):
        """Predict the category of a question"""
        X = self.vectorizer.transform([question])
        pred = self.category_classifier.predict(X)[0]
        return self.category_encoder.inverse_transform([pred])[0]
    
    def generate_follow_up(self, question, answer_quality='medium'):
        """Generate a follow-up question based on the original question"""
        # Predict category and difficulty
        category = self.predict_category(question)
        difficulty = self.predict_difficulty(question)
        
        # Adjust difficulty based on answer quality
        difficulty_levels = ['easy', 'medium', 'hard']
        current_idx = difficulty_levels.index(difficulty)
        
        if answer_quality == 'good' and current_idx < 2:
            new_difficulty = difficulty_levels[current_idx + 1]
        elif answer_quality == 'poor' and current_idx > 0:
            new_difficulty = difficulty_levels[current_idx - 1]
        else:
            new_difficulty = difficulty
        
        # Get a related question
        related = self.questions_db[
            (self.questions_db['category'] == category) &
            (self.questions_db['difficulty'] == new_difficulty)
        ]
        
        if len(related) > 0:
            return related.sample(1)['question'].values[0]
        else:
            return None

def main():
    """Main training function"""
    print("=" * 60)
    print("🎯 INTERVIEW QUESTION MODEL TRAINER")
    print("=" * 60)
    
    # Initialize model
    model = InterviewModel()
    
    # Load data
    df = model.load_data('interview_questions.csv')
    
    # Train model
    model.train(df)
    
    # Save model
    model.save_model('model')
    
    print("\n" + "=" * 60)
    print("🎉 TRAINING COMPLETE!")
    print("=" * 60)
    print("\n📊 Model Statistics:")
    print(f"   - Total questions: {len(df)}")
    print(f"   - Technical questions: {len(df[df['category'] == 'Technical'])}")
    print(f"   - Behavioral questions: {len(df[df['category'] == 'Behavioral'])}")
    print(f"   - Easy: {len(df[df['difficulty'] == 'easy'])}")
    print(f"   - Medium: {len(df[df['difficulty'] == 'medium'])}")
    print(f"   - Hard: {len(df[df['difficulty'] == 'hard'])}")
    
    print("\n💡 Next steps:")
    print("   1. Run 'python app.py' to start the interview server")
    print("   2. Open the web interface in your browser")
    print("   3. Start conducting AI-powered interviews!")

if __name__ == "__main__":
    main()
