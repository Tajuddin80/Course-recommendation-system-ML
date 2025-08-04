# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import io
from model.recommender import recommend_courses_for_users

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB upload limit

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    try:
        file = request.files['file']
        content = file.read().decode('utf-8')

        print("--- Uploaded CSV content start ---")
        print(content)
        print("--- Uploaded CSV content end ---")

        # Removed sep=',' to properly handle quoted delimiters
        users_df = pd.read_csv(
            io.StringIO(content),
            quotechar='"',
            engine='python',
            on_bad_lines='skip'
        )

        if 'interests' not in users_df.columns:
            return jsonify({'error': 'CSV must contain "interests" column'}), 400

        results = recommend_courses_for_users(users_df)
        return jsonify(results)

    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
