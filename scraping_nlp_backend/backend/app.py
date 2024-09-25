from flask import Flask, request, jsonify
from scraping.review_scraper import scrape_reviews
from nlp.sentiment_analyzer import analyze_sentiment  # Import the sentiment analyzer

app = Flask(__name__)

@app.route('/scrape_reviews', methods=['POST'])
def scrape_reviews_api():
    data = request.json
    product_link = data.get('product_link')
    
    if product_link:
        review_summaries = scrape_reviews(product_link)
        sentiment_summary = analyze_sentiment(review_summaries)
        return jsonify({"summary": sentiment_summary}), 200
    else:
        return jsonify({"error": "Product link is required."}), 400

if __name__ == "__main__":
    app.run(debug=True)
