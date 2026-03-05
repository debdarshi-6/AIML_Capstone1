from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from scipy.sparse import csr_matrix, hstack
from fastapi.middleware.cors import CORSMiddleware
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import StandardScaler

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scaler = StandardScaler()

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

# Load models and vectorizer
dept_model = joblib.load("department_new.pkl")
priority_model = joblib.load("priority_new.pkl")
tfidf = joblib.load("tfidf.pkl")


dept_mapping = {
    0: "Account",
    1: "Billing",
    2: "Feedback",
    3: "Sales",
    4: "Tech"
}

priority_map = {
    0: "High",
    1: "Low",
    2: "Medium"
}

class TicketRequest(BaseModel):
    ticket_text: str


@app.get("/")
def home():
    return {"message": "API is running 🚀"}


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', str(text))

    tokens = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and len(token) > 2]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return ' '.join(tokens)


@app.post("/predict")
def predict_ticket(data: TicketRequest):
    try:
        # print("Received text:", data.ticket_text)

        cleaned_ticket = preprocess_text(data.ticket_text)
        print("Cleaned:", cleaned_ticket)

        ticket_tfidf = tfidf.transform([cleaned_ticket])
        print("TFIDF shape:", ticket_tfidf.shape)
        
        new_tenure = 12
        tenure_scaled = scaler.fit_transform([[new_tenure]])

        # dummy_features = np.array([[30, 1, 1]])
        # print("Dummy shape:", dummy_features.shape)
        final_input = hstack([ticket_tfidf, csr_matrix(tenure_scaled)])
        # ticket_features = hstack([ticket_tfidf, dummy_features])
        # print("Final feature shape:", ticket_features.shape)

        dept_prediction = dept_model.predict(final_input)
        priority_prediction = priority_model.predict(final_input)

        return {
            "Department": dept_mapping[int(dept_prediction)],
            "Priority": priority_map[int(priority_prediction)]
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}