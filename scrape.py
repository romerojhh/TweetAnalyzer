import requests
from bs4 import BeautifulSoup

# Twitter profile URL
url = "https://twitter.com/SeattlePD"

# Custom user agent string
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

# Set the headers with the custom user agent
headers = {"User-Agent": user_agent}

# Send a request to the URL
response = requests.get(url, headers=headers)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all tweet elements
tweets = soup.find_all("div", class_="tweet")
print(soup)

# Extract tweet data
for tweet in tweets:
    tweet_text = tweet.find("div", class_="tweet-text").get_text()
    tweet_date = tweet.find("span", class_="_timestamp").get_text()
    # Extract other desired data
    print(f"Tweet: {tweet_text}\nDate: {tweet_date}\n")