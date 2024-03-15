# E-Commerce Sentiment Analysis System

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-VADER-FF6B35?style=flat)

An NLP-powered web application that analyzes sentiment of Amazon and Yelp customer reviews at scale. Upload a CSV of thousands of reviews — get instant sentiment classification and interactive visualizations.

> Built during Masters studies at UNC Charlotte as part of an NLP course project.

---

## Why This Exists

E-commerce companies lose millions due to unaddressed negative reviews. Reading them manually doesn't scale. This system automates sentiment classification and surfaces trends so businesses can act fast.

---

## How It Works

```
User submits review or uploads CSV
          ↓
VADER analyzes each review using built-in lexicon
          ↓
Compound score calculated per review
          ↓
Classified as Positive / Negative / Neutral
          ↓
Results stored in SQLite database
          ↓
Interactive Plotly charts render trends
```

---

## VADER Scoring

| Score | Sentiment |
|---|---|
| >= 0.05 | Positive |
| <= -0.05 | Negative |
| Between -0.05 and 0.05 | Neutral |

VADER handles capitalization, punctuation, negations, slang, and emojis — making it ideal for informal review text.

---

## Why VADER over BERT?

| Factor | VADER | BERT |
|---|---|---|
| Training data | Not required | Large dataset needed |
| Speed | Real-time | Slow, GPU needed |
| Best for | Social media, reviews | General NLP |
| Handles slang/emojis | Yes | Needs preprocessing |
| Cost | Free, runs locally | Expensive at scale |
| Privacy | Data stays local | Sent to external API |

For short, informal, emoji-heavy e-commerce reviews — VADER gives 80% of BERT accuracy at 1% of the cost.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Flask-CORS |
| NLP | VADER Sentiment Analysis |
| Database | SQLite |
| Visualization | Plotly |
| Frontend | HTML, CSS, JavaScript |
| Data | Pandas |

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/analyze` | POST | Analyze a single review |
| `/analyze/bulk` | POST | Bulk analyze CSV file |
| `/charts/distribution` | GET | Sentiment distribution pie chart |
| `/charts/trend` | GET | Sentiment trend over time |
| `/charts/scores` | GET | Average scores by sentiment |
| `/stats` | GET | Overall statistics |

---

## Setup & Run

```bash
pip install flask flask-cors pandas vaderSentiment plotly

# Run the Flask server
python app.py

# In a new terminal, serve the frontend
python3 -m http.server 3001
```

Visit `http://localhost:3001` in your browser.

---

## CSV Format

Your CSV must have one of these column names: `review`, `text`, or `Review`.
A `sample_reviews.csv` with 20 Amazon and Yelp reviews is included for testing.

---

## Project Structure

```
ecommerce-sentiment-analysis/
├── app.py              # Flask backend + VADER pipeline
├── index.html          # Frontend UI
├── sample_reviews.csv  # Sample Amazon reviews
├── yelp_reviews.csv    # Sample Yelp reviews
├── .gitignore
└── README.md
```

---

## What's Next

- BERT integration for higher accuracy on complex reviews
- Aspect-based sentiment — identify sentiment per product feature
- Real-time dashboard with live streaming reviews
- Multi-language support
- Docker deployment

---

## Author

**Soumya Reddy Gaddam**
Data Engineer | AWS Certified | MSCS @ UNC Charlotte

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/gsred)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/gsoumyar)