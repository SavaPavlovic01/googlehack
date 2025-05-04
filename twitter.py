import requests
import re

def extract_id_from_url(url):
    """
    Extracts the ID at the end of a URL.

    Args:
        url: The URL string.

    Returns:
        The ID at the end of the URL as a string, or None if no ID is found.
    """
    match = re.search(r'/([^/]+)$', url)
    if match:
        return match.group(1)
    else:
        return None
  
def get_tweet_text(url):
    id = extract_id_from_url(url)
    url = f"https://cdn.syndication.twimg.com/tweet-result?id={id}&token=a"

    r = requests.get(url)

    data = r.json()

    return data["text"]

if __name__ == "__main__":
    print(get_tweet_text("https://x.com/MrKimmKE/status/1918582688979493122"))