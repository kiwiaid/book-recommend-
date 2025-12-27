import pandas as pd

def load_and_clean_data(path):
    df = pd.read_csv(path, on_bad_lines='skip')

    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    df['Book'] = df['Book'].fillna('')
    df['Author'] = df['Author'].fillna('')
    df['Genres'] = df['Genres'].fillna('')
    df['Description'] = df['Description'].fillna('')

    return df


import pandas as pd


def load_and_clean_data(file_path):
    # 1️⃣ Load dataset
    df = pd.read_csv(file_path, on_bad_lines='skip')

    # 2️⃣ Drop unnecessary column
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    # 3️⃣ Handle missing text fields
    df['Description'] = df['Description'].fillna('')
    df['Genres'] = df['Genres'].fillna('')

    # 🔴 PUT YOUR CODE HERE (THIS IS THE RIGHT PLACE)
    # 4️⃣ Convert numeric columns safely
    df['Num_Ratings'] = pd.to_numeric(df['Num_Ratings'], errors='coerce').fillna(0)
    df['Avg_Rating'] = pd.to_numeric(df['Avg_Rating'], errors='coerce').fillna(0)

    # 5️⃣ Remove duplicate books
    df.drop_duplicates(subset=['Book'], inplace=True)

    return df
