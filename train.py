# ==========================================
# CAPSTONE 8 – MULTI-TARGET CLASSIFICATION
# TF-IDF vs ANN vs Frozen BERT
# (Department + Priority)
# ==========================================

import pandas as pd
import numpy as np
import time
import re

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression

from scipy.sparse import hstack, csr_matrix
from sentence_transformers import SentenceTransformer


# --------------------------------
# 1. LOAD DATA
# --------------------------------
def load_data():
    df = pd.read_csv("tickets_modified_with_priority.csv")
    print("Dataset Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    return df


# --------------------------------
# 2. CLEAN TEXT
# --------------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# --------------------------------
# 3. PREPROCESS
# --------------------------------
def preprocess(df):

    print("\nCleaning text...")
    df["ticket_text"] = df["ticket_text"].apply(clean_text)

    print("\nDepartment distribution:")
    print(df["department"].value_counts())

    print("\nPriority distribution:")
    print(df["priority"].value_counts())

    # Encode targets
    dept_encoder = LabelEncoder()
    priority_encoder = LabelEncoder()

    y_dept = dept_encoder.fit_transform(df["department"])
    y_priority = priority_encoder.fit_transform(df["priority"])

    # Scale numeric feature
    scaler = StandardScaler()
    X_num = scaler.fit_transform(df[["tenure"]])

    return df, X_num, y_dept, y_priority


# --------------------------------
# GENERIC TRAIN FUNCTION
# --------------------------------
def train_and_evaluate(X, y, model, model_name, target_name):

    print(f"\n====== {model_name} ({target_name}) ======")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    start = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start

    start = time.time()
    preds = model.predict(X_test)
    infer_time = time.time() - start

    print("Accuracy:", round(accuracy_score(y_test, preds), 4))
    print("Train Time:", round(train_time, 2), "sec")
    print("Inference Time:", round(infer_time, 4), "sec")


# --------------------------------
# MAIN
# --------------------------------
def main():

    df = load_data()

    df, X_num, y_dept, y_priority = preprocess(df)

    print("\nCreating TF-IDF features...")
    tfidf = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        stop_words="english"
    )

    X_text = tfidf.fit_transform(df["ticket_text"])

    # ==============================
    # TF-IDF Models
    # ==============================
    X_sparse = hstack([X_text, csr_matrix(X_num)])

    train_and_evaluate(
        X_sparse,
        y_dept,
        LinearSVC(class_weight="balanced"),
        "TF-IDF",
        "Department"
    )

    train_and_evaluate(
        X_sparse,
        y_priority,
        LinearSVC(class_weight="balanced"),
        "TF-IDF",
        "Priority"
    )

    # ==============================
    # ANN Models
    # ==============================
    X_dense = X_sparse.toarray()

    train_and_evaluate(
        X_dense,
        y_dept,
        MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=20, random_state=42),
        "ANN",
        "Department"
    )

    train_and_evaluate(
        X_dense,
        y_priority,
        MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=20, random_state=42),
        "ANN",
        "Priority"
    )

    # ==============================
    # BERT (Frozen)
    # ==============================
    print("\nGenerating BERT embeddings...")
    bert_model = SentenceTransformer("all-MiniLM-L6-v2")

    start = time.time()
    embeddings = bert_model.encode(
        df["ticket_text"].tolist(),
        batch_size=32,
        show_progress_bar=True
    )
    embed_time = time.time() - start

    print("Embedding Time:", round(embed_time, 2), "sec")

    X_bert = hstack([csr_matrix(embeddings), csr_matrix(X_num)])

    train_and_evaluate(
        X_bert,
        y_dept,
        LogisticRegression(max_iter=300),
        "BERT (Frozen)",
        "Department"
    )

    train_and_evaluate(
        X_bert,
        y_priority,
        LogisticRegression(max_iter=300),
        "BERT (Frozen)",
        "Priority"
    )


if __name__ == "__main__":
    main()