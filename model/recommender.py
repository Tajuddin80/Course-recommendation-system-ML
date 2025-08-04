import pandas as pd

def recommend_courses_for_users(user_df):
    # Load the detailed courses CSV
    courses = pd.read_csv('courses.csv')

    results = []

    for _, user_row in user_df.iterrows():
        user_id = user_row.get('user_id', 'N/A')
        interests = user_row.get('interests', '')

        if pd.isna(interests):
            results.append({
                "user_id": user_id,
                "recommendations": []
            })
            continue

        # User interests as lowercase keywords list
        keywords = [kw.strip().lower() for kw in interests.split(';')]

        recommendations = []

        for _, course_row in courses.iterrows():
            # Extract searchable fields and make lowercase strings
            subject = str(course_row.get('subject', '')).lower()
            title = str(course_row.get('course_title', '')).lower()
            # You could also add description or other fields if you want
            
            # Combine searchable text
            searchable_text = ' '.join([subject, title])

            # Calculate score as count of keywords present in searchable_text
            score = sum(1 for kw in keywords if kw in searchable_text)

            if score > 0:
                recommendations.append({
                    'course_id': course_row.get('course_id'),
                    'title': course_row.get('course_title'),
                    'url': course_row.get('url'),
                    'price': course_row.get('price'),
                    'is_paid': course_row.get('is_paid'),
                    'score': score
                })

        # Sort recommendations by score descending
        recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)

        results.append({
            'user_id': user_id,
            'recommendations': recommendations
        })

    return results
