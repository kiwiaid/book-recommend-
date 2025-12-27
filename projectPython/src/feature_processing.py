from sklearn.feature_extraction.text import TfidfVectorizer

def create_tfidf(df):
    df['content'] = (
        df['Book'] + ' ' +
        df['Author'] + ' ' +
        df['Genres'] + ' ' +
        df['Description']
    )

    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=5000
    )

    tfidf_matrix = vectorizer.fit_transform(df['content'])

    return tfidf_matrix
