import pandas as pd
import matplotlib.pyplot as plt
import os

def extract_features_and_plot(df):
    # Clean and extract
    df['Gene'] = df['Gene Variant / Mutation Identified'].str.split().str[0]
    df['DNA Change Type'] = df['Type of DNA Change'].str.strip()
    df['Implication'] = df['Implication'].str.strip()

    # Plot: Type of DNA Change count
    plt.figure(figsize=(10,5))
    df['DNA Change Type'].value_counts().plot(kind='bar', color='skyblue')
    plt.title('Distribution of DNA Change Types')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/graph.png')


extract_features_and_plot(df)
