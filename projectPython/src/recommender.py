from sklearn.metrics.pairwise import cosine_similarity

def build_similarity(tfidf_matrix):
    return cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_books(book_title, df, cosine_sim, top_n=5):
    matches = df[df['Book'].str.lower() == book_title.lower()]

    if matches.empty:
        return "Book not found. Check the title spelling."

    idx = matches.index[0]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]

    recommendations = []

    for i, score in sim_scores:
        shared_genres = set(df.loc[idx, 'Genres'].split(',')) & set(df.loc[i, 'Genres'].split(','))

        recommendations.append({
            'Book': df.loc[i, 'Book'],
            'Author': df.loc[i, 'Author'],
            'Genres': df.loc[i, 'Genres'],
            'Avg_Rating': df.loc[i, 'Avg_Rating'],
            'Similarity_Score': round(score, 3),
            'Reason': f"Shares genres: {', '.join(shared_genres) if shared_genres else 'Similar content'}"
        })

    return recommendations
