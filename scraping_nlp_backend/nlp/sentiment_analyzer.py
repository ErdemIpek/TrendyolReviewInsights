from openai import OpenAI
# Initialize the OpenAI API client

client = OpenAI(
    api_key=':)',
)
def analyze_sentiment(reviews):
   
    prompt = (
        "You are an assistant that analyzes product reviews. "
        "Based on the following reviews, provide a concise summary and suggestions.\n\n"
        "Reviews:\n"
    )
    
    for review in reviews:
        prompt += f"- {review['comment']}\n"
    
    prompt += (
        "\nProvide insights such as size recommendations, common complaints, and general advice for potential buyers."
    )
    
    try:
       
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or whichever model you prefer
            messages=[{"role": "user", "content": prompt}],
           
        )

       
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        print(f"Error while calling OpenAI API: {e}")
        return "Unable to analyze sentiment."

if __name__ == "__main__":
   
    
    print(":)")
