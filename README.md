# E-Commerce Sentiment Analysis System

An NLP-powered web application to analyze sentiment of Amazon and Yelp customer reviews using VADER sentiment analysis. Built as part of an NLP course project during Masters studies at University of North Carolina Charlotte.

## Why This Project?
E-commerce companies lose millions due to unaddressed negative reviews. Manual review reading does not scale to 100K+ reviews. This system automates sentiment classification at scale and visualizes trends to help businesses make data-driven decisions faster.

## Why VADER over BERT?

| Factor | VADER | BERT |
|---|---|---|
| Training data | Not required | Large labeled dataset needed |
| Speed | Real-time | Slow (GPU needed) |
| Best for | Social media, e-commerce text | General purpose NLP |
| Handles slang/emojis | Yes | Needs preprocessing |
| Cost | Free, runs locally | Expensive at scale |
| Privacy | Data stays local | Sent to external API |

For e-commerce reviews which are short, informal and emoji-heavy, VADER gives 80% of BERT accuracy at 1% of the cost and complexity. BERT makes more sense when you need aspect-level sentiment or multilingual support.

## Why Not Just Use ChatGPT API?
- ChatGPT costs money per review - 100K reviews gets expensive fast
- Data privacy concerns - customer reviews contain sensitive business data
- VADER runs locally, completely free, with no rate limits
- No dependency on external API availability

## How It Works
1. Enter a single review or upload a CSV of reviews
2. VADER analyzes each review using its built-in lexicon
3. Returns Positive, Negative, or Neutral with confidence scores
4. Results stored in SQLite database (simulating Google BigQuery)
5. Interactive Plotly charts show sentiment distribution and trends

## VADER Scoring
- **Compound score >= 0.05** - Positive
- **Compound score <= -0.05** - Negative
- **Between -0.05 and 0.05** - Neutral

VADER handles:
- Capitalization ("AMAZING" vs "amazing")
- Punctuation ("Great!!!" vs "Great")
- Negations ("not good" = negative)
- Slang and emojis

## Tech Stack
- **Backend**: Python, Flask, Flask-CORS
- **NLP**: VADER Sentiment Analysis (vaderSentiment)
- **Database**: SQLite (simulating Google BigQuery for local development)
- **Visualization**: Plotly (originally Tableau, ported to Plotly for web deployment)
- **Frontend**: HTML, CSS, JavaScript
- **Data**: Pandas, sample Amazon and Yelp reviews dataset

## API Endpoints
- `POST /analyze` - Analyze a single review
- `POST /analyze/bulk` - Bulk analyze CSV file
- `GET /charts/distribution` - Sentiment distribution pie chart
- `GET /charts/trend` - Sentiment trend over time
- `GET /charts/scores` - Average scores by sentiment category
- `GET /stats` - Overall statistics

## Setup

```bash
pip install flask flask-cors pandas vaderSentiment plotly

# Run the Flask server
python app.py

# In a new terminal, serve the frontend
python3 -m http.server 3001
```

Visit `http://localhost:3001` in your browser.

## CSV Format
Your CSV must have one of these column names: `review`, `text`, or `Review`.
A `sample_reviews.csv` with 20 Amazon and Yelp reviews is included for testing.

## Note on Visualization
Initial analysis and exploration was done in Tableau Desktop for rich dashboarding. Interactive charts were rebuilt in Plotly for web deployment and GitHub sharing, as Tableau requires a licensed server for embedding.

## Current Limitations & Future Improvements
This is a basic version using VADER. It can be significantly improved with:
- **BERT Integration** - transformer models for higher accuracy on complex reviews
- **Real BigQuery** - connect to Google BigQuery for 100K+ reviews at scale
- **Aspect-based Sentiment** - identify sentiment for specific product aspects (battery, design, price)
- **Multi-language Support** - analyze reviews in Spanish, French, German etc.
- **Real-time Dashboard** - live updating charts as new reviews stream in
- **Docker Deployment** - containerize for easy cloud deployment
- **Review Summarization** - use LLMs to generate executive summaries of sentiment trends
- **Alert System** - notify teams when negative sentiment spikes above threshold