import zipfile
import os
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

zip_path = "resep.zip"
extract_path = "resep_dataset"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

os.listdir(extract_path)

csv_files = [f for f in os.listdir(extract_path) if f.endswith(".csv")]

dataframes = []
for file in csv_files:
    df = pd.read_csv(os.path.join(extract_path, file))
    df["kategori"] = file.replace("dataset-", "").replace(".csv", "")
    dataframes.append(df)

resep_df = pd.concat(dataframes, ignore_index=True)

resep_df.head()

def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    return text

resep_df["clean_ingredients"] = resep_df["Ingredients"].apply(preprocess)
resep_df["clean_title"] = resep_df["Title"].apply(preprocess)


vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(resep_df["clean_title"])

def cari_resep_berdasarkan_judul(query, top_n=5):
    query_clean = re.sub(r'[^a-z\s]', ' ', query.lower())
    query_vec = vectorizer.transform([query_clean])

    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[::-1][:top_n]

    results = resep_df.iloc[top_indices][["Title", "kategori", "Ingredients"]].copy()
    results["Skor Kemiripan"] = similarities[top_indices]

    return results


def highlight_title_html(title, query_words):
    title = str(title)
    for word in query_words:
        pattern = re.compile(rf'\b({re.escape(word)})\b', flags=re.IGNORECASE)
        title = pattern.sub(r'<mark>\1</mark>', title)
    return title