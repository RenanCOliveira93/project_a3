from etl import *
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd

df_sample = df_rating4.sample(n=300000, random_state=42)  # Amostra de 300.000 linhas

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

print("Aplicando o Vader na coluna 'summary'")
df_sample['sentiment_summary'] = df_sample['summary'].apply(lambda x: sia.polarity_scores(x)['compound'])
# Classificar as avaliações como positivas ou negativas
print("Classificando entre negativo e positivo")
df_sample['sentiment_label_summary'] = df_sample['sentiment_summary'].apply(lambda score: 'positive' if score >= 0 else 'negative')

print("Aplicando o Vader na coluna 'text'")
df_sample['sentiment_text'] = df_sample['text'].apply(lambda x: sia.polarity_scores(x)['compound'])
print("Classificando entre negativo e positivo")
df_sample['sentiment_label_text'] = df_sample['sentiment_text'].apply(lambda score: 'positive' if score >= 0 else 'negative')

df5 = df4[['Title', 'description', 'authors', 'categories', 'publisher', 'publishedDate']]
df5['authors'] = df5['authors'].str.replace("['", "")
df5['authors'] = df5['authors'].str.replace("']", "")
df5['categories'] = df5['categories'].str.replace("['", "")
df5['categories'] = df5['categories'].str.replace("']", "")
df5['authors'] = df5['authors'].str.replace("'", "")
df5['categories'] = df5['categories'].str.replace("'", "")

merged_df = pd.merge(df5, df_sample, on='Title')