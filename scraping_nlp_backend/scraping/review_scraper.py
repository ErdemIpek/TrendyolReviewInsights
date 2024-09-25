import requests
import json
import re
from urllib.parse import urlparse, parse_qs

class ReviewScraper:
    def __init__(self, product_link):
        self.product_link = product_link
        self.reviews = []
    
    def get_reviews(self):
        
        parsed_url = urlparse(self.product_link)
        query_params = parse_qs(parsed_url.query)

     
        product_id = parsed_url.path
        boutique_id = query_params.get('boutiqueId', [''])[0]
        merchant_id = query_params.get('merchantId', [''])[0]
        
      
        reviews_api_url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/reviews{product_id}/yorumlar"
        
      
        response = requests.get(reviews_api_url)
        if response.status_code == 200:
            self.reviews = response.json()
        else:
            print(f"Failed to fetch reviews: {response.status_code}")

    def extract_reviews(self):
        
        hydrate_script = self.reviews.get('result', {}).get('hydrateScript', '')
        
        # Extract the JSON object from the hydrateScript string
        json_data_match = re.search(r'window\.__REVIEW_APP_INITIAL_STATE__ = (.*?);', hydrate_script)
        
        if json_data_match:
            json_data = json_data_match.group(1)
            review_data = json.loads(json_data)
            return review_data['ratingAndReviewResponse']['ratingAndReview']['productReviews']['content']
        return []

    def summarize_reviews(self):
        summaries = []
        for review in self.extract_reviews():
            summary = {
                'user': review.get('userFullName'),
                'rate': review.get('rate'),
                'comment': review.get('comment'),
                'comment_date': review.get('commentDateISOtype'),
                'product_size': review.get('productSize')
            }
            summaries.append(summary)
        return summaries

    def run(self):
        self.get_reviews()
        return self.summarize_reviews()


def scrape_reviews(product_link):
    scraper = ReviewScraper(product_link)
    return scraper.run()


if __name__ == "__main__":
    product_link = "https://www.trendyol.com/imprime/muse-edp-kadin-parfum-ciceksi-meyveli-frenk-uzumu-lavanta-yasemin-vanilya-misk-amber-50ml-p-279708971"
    
    review_summaries = scrape_reviews(product_link)

    for review in review_summaries:
        print(review)
