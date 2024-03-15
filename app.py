from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import sqlite3
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
from plotly.io import to_json
import io
import csv

app = Flask(__name__)
CORS(app)

analyzer = SentimentIntensityAnalyzer()

def init_db():
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  review TEXT,
                  source TEXT,
                  sentiment TEXT,
                  positive REAL,
                  negative REAL,
                  neutral REAL,
                  compound REAL,
                  created_at DATE DEFAULT CURRENT_DATE)''')
    conn.commit()
    conn.close()

init_db()

def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        sentiment = 'Positive'
    elif compound <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    return {
        'sentiment': sentiment,
        'positive': round(scores['pos'], 3),
        'negative': round(scores['neg'], 3),
        'neutral': round(scores['neu'], 3),
        'compound': round(compound, 3)
    }

def save_to_db(review, source, result, date=None):
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    if date:
        c.execute('''INSERT INTO reviews (review, source, sentiment, positive, negative, neutral, compound, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (review, source, result['sentiment'], result['positive'],
                   result['negative'], result['neutral'], result['compound'], date))
    else:
        c.execute('''INSERT INTO reviews (review, source, sentiment, positive, negative, neutral, compound)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (review, source, result['sentiment'], result['positive'],
                   result['negative'], result['neutral'], result['compound']))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({"message": "E-Commerce Sentiment Analysis API is running!"})

@app.route('/analyze', methods=['POST'])
def analyze_single():
    data = request.get_json()
    review = data.get('review', '').strip()
    source = data.get('source', 'Manual')
    if not review:
        return jsonify({'error': 'Review text is required'}), 400
    result = analyze_sentiment(review)
    save_to_db(review, source, result)
    return jsonify({
        'review': review,
        'source': source,
        'sentiment': result['sentiment'],
        'scores': {
            'positive': result['positive'],
            'negative': result['negative'],
            'neutral': result['neutral'],
            'compound': result['compound']
        }
    })

@app.route('/analyze/bulk', methods=['POST'])
def analyze_bulk():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    source = request.form.get('source', 'CSV Upload')
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files accepted'}), 400
    stream = io.StringIO(file.stream.read().decode('utf-8'))
    reader = csv.DictReader(stream)
    results = []
    for row in reader:
        review_text = row.get('review') or row.get('text') or row.get('Review') or list(row.values())[0]
        date = row.get('date') or row.get('Date') or None
        if not review_text:
            continue
        result = analyze_sentiment(str(review_text))
        save_to_db(str(review_text), source, result, date)
        results.append({
            'review': str(review_text)[:100] + '...' if len(str(review_text)) > 100 else str(review_text),
            'sentiment': result['sentiment'],
            'compound': result['compound']
        })
    df = pd.DataFrame(results)
    summary = df['sentiment'].value_counts().to_dict() if not df.empty else {}
    return jsonify({
        'total_analyzed': len(results),
        'summary': summary,
        'results': results[:50]
    })

@app.route('/charts/distribution', methods=['GET'])
def chart_distribution():
    conn = sqlite3.connect('sentiment.db')
    df = pd.read_sql_query("SELECT sentiment, COUNT(*) as count FROM reviews GROUP BY sentiment", conn)
    conn.close()
    if df.empty:
        return jsonify({'error': 'No data yet'}), 404
    # Return plain JSON instead of Plotly binary format
    return jsonify({
        'labels': df['sentiment'].tolist(),
        'values': df['count'].tolist(),
        'type': 'pie'
    })

@app.route('/charts/trend', methods=['GET'])
def chart_trend():
    conn = sqlite3.connect('sentiment.db')
    df = pd.read_sql_query("""
        SELECT created_at as date, sentiment, COUNT(*) as count
        FROM reviews GROUP BY created_at, sentiment ORDER BY created_at
    """, conn)
    conn.close()
    if df.empty:
        return jsonify({'error': 'No data yet'}), 404
    result = {}
    for _, row in df.iterrows():
        s = row['sentiment']
        if s not in result:
            result[s] = {'dates': [], 'counts': []}
        result[s]['dates'].append(str(row['date']))
        result[s]['counts'].append(int(row['count']))
    return jsonify(result)

@app.route('/charts/scores', methods=['GET'])
def chart_scores():
    conn = sqlite3.connect('sentiment.db')
    df = pd.read_sql_query("""
        SELECT sentiment, AVG(positive) as avg_positive,
               AVG(negative) as avg_negative, AVG(neutral) as avg_neutral
        FROM reviews GROUP BY sentiment
    """, conn)
    conn.close()
    if df.empty:
        return jsonify({'error': 'No data yet'}), 404
    return jsonify({
        'sentiments': df['sentiment'].tolist(),
        'positive': [round(x,3) for x in df['avg_positive'].tolist()],
        'negative': [round(x,3) for x in df['avg_negative'].tolist()],
        'neutral': [round(x,3) for x in df['avg_neutral'].tolist()]
    })

@app.route('/stats', methods=['GET'])
def stats():
    conn = sqlite3.connect('sentiment.db')
    total = pd.read_sql_query("SELECT COUNT(*) as count FROM reviews", conn).iloc[0]['count']
    by_sentiment = pd.read_sql_query("SELECT sentiment, COUNT(*) as count FROM reviews GROUP BY sentiment", conn)
    by_source = pd.read_sql_query("SELECT source, COUNT(*) as count FROM reviews GROUP BY source", conn)
    conn.close()
    return jsonify({
        'total_reviews': int(total),
        'by_sentiment': by_sentiment.to_dict('records'),
        'by_source': by_source.to_dict('records')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)