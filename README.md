# E-Commerce Sentiment Analysis

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-VADER-orange?style=flat)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![REST API](https://img.shields.io/badge/REST%20API-009688?style=flat)

A full-stack sentiment analysis web app for e-commerce reviews. Accepts customer reviews via REST API, classifies them as Positive, Negative, or Neutral using VADER NLP, and visualizes results with interactive Plotly charts.

---

## Why I Built This

Understanding customer sentiment at scale is a core problem in every product-driven company. Instead of manual review reading, this app processes hundreds of reviews instantly and surfaces patterns — helping teams prioritize product improvements.

---

## Features

- **REST API** — POST endpoint accepts review text, returns sentiment score and label
- **VADER NLP** — Rule-based sentiment engine optimized for short, informal text
- **Interactive Dashboard** — Plotly bar and pie charts showing sentiment distribution
- **CSV Upload** — Bulk analyze review datasets in one click
- **No ML training required** — Runs instantly, no GPU or model downloads needed

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| NLP Engine | VADER (Valence Aware Dictionary) |
| Data Processing | Pandas |
| Visualization | Plotly |
| Frontend | HTML, CSS, JavaScript |

---

## System Design

```
User/CSV Input
      │
      ▼
  Flask API
      │
      ▼
VADER NLP Engine
      │
   ┌──┴──┐
   │     │
Score  Label
(-1 to +1) (Pos/Neg/Neutral)
      │
      ▼
  Plotly Charts
      │
      ▼
  Dashboard UI
```

---

## API Usage

**Analyze a single review:**
```bash
POST /analyze
Content-Type: application/json

{
  "review": "The product quality is amazing, fast delivery too!"
}
```

**Response:**
```json
{
  "text": "The product quality is amazing, fast delivery too!",
  "sentiment": "POSITIVE",
  "score": 0.82,
  "compound": 0.7184
}
```

**Bulk analyze from CSV:**
```bash
POST /upload
Form-data: file=reviews.csv
```

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/soumyagdev/ecommerce-sentiment-analysis.git
cd ecommerce-sentiment-analysis

# Install dependencies
pip install flask vaderSentiment pandas plotly

# Run the app
python app.py

# Open browser
http://localhost:5000
```

---

## Sample Output

| Review | Sentiment | Score |
|--------|-----------|-------|
| "Great quality, love it!" | POSITIVE | 0.84 |
| "Broke after 2 days, terrible." | NEGATIVE | -0.72 |
| "Package arrived on time." | NEUTRAL | 0.12 |

---

## What I Learned

- Building and consuming REST APIs with Flask
- Text preprocessing and NLP pipeline design
- Data visualization with Plotly
- Handling CSV file uploads in web applications
- Designing systems that scale from 1 review to 10,000+

---

## Author

**Soumya Reddy Gaddam**
Software Engineer | Python · Flask · NLP · REST APIs

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/soumyagdev)