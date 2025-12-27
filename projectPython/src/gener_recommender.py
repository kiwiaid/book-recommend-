def calculate_genre_popularity(df):
    """
    Calculate genre popularity using number of ratings.
    """
    genre_scores = {}

    for _, row in df.iterrows():
        if not isinstance(row['Genres'], str):
            continue

        try:
            num_ratings = int(row['Num_Ratings'])
        except (ValueError, TypeError):
            num_ratings = 0

        genres = [g.strip() for g in row['Genres'].split(',')]

        for genre in genres:
            genre_scores[genre] = genre_scores.get(genre, 0) + num_ratings

    return genre_scores


def recommend_by_genre(book_title, df, top_n=5):
    """
    Recommend books based on shared genres.
    """
    book_title = book_title.lower()

    matches = df[df['Book'].str.lower().str.contains(book_title)]
    if matches.empty:
        return "❌ Book not found in dataset."
    selected_book = matches.iloc[0]


    if not isinstance(selected_book['Genres'], str):
        return "❌ No genre data available for this book."

    selected_genres = set(g.strip() for g in selected_book['Genres'].split(','))

    recommendations = []

    for _, row in df.iterrows():
        if row['Book'].lower() == book_title:
            continue

        if not isinstance(row['Genres'], str):
            continue

        book_genres = set(g.strip() for g in row['Genres'].split(','))

        common_genres = selected_genres.intersection(book_genres)

        if common_genres:
            recommendations.append({
                "Book": row['Book'],
                "Author": row['Author'],
                "Avg_Rating": row['Avg_Rating'],
                "Reason": f"Shares genres: {', '.join(common_genres)}"
            })

    # Sort by rating
    recommendations = sorted(
        recommendations,
        key=lambda x: x['Avg_Rating'],
        reverse=True
    )

    return recommendations[:top_n]
