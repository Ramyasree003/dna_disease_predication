import pandas as pd

# Load data
df = pd.read_csv('static/dataset/dataset.csv')  # Or read_excel() if from Excel

# Clean columns
df.columns = [col.strip() for col in df.columns]
df = df.drop_duplicates()

# Extract gene name
df['Gene'] = df['Gene Variant / Mutation Identified'].str.split().str[0]

# Encode mutation type
df['DNA Change Type Encoded'] = df['Type of DNA Change'].astype('category').cat.codes

# Encode implication
implication_map = {
    'Protective effect': 0,
    'Carrier': 1,
    'Moderate risk': 2,
    'Increased risk': 3,
    'High predisposition': 4
}
df['Implication Encoded'] = df['Implication'].map(implication_map)

# Preview
print(df.head())
