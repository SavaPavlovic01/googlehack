import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    ret = [] 
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    titles = soup.find_all('h2', {'class':'news-item-title'})
    for title in titles:
        ret.append(title.get_text())
    return ret

def scrape_politika():
    url_base = "https://informer.rs/politika?page="
    informer_titles = []
    # 17 jer toliko ima :(
    for i in range(17):
        cur_url = url_base + str(i)
        resp = requests.get(cur_url)
        soup = BeautifulSoup(resp.text)
        titles = soup.find_all('h2', {'class':'news-item-title'})

        # prvih 30 je politika ostalo je neki krs
        for title in titles:
            informer_titles.append(title.get_text())
    return informer_titles
# OSTAJE SLEDECA VEST I NEKI NONE NA KRAJU
def scrape_text(url):
    exclude = ["platforms-box", "related-news", "leave-comment-action", "top-box-sidebar", "tags-box", "next-news-item active", "comments-rules", "news-item-data", "end-of-news", "leave-comment"]
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    target = soup.find(class_="single-news-content")

    if target:
        # Remove all elements with the excluded class names
        for class_name in exclude:
            for tag in target.find_all(class_=class_name):
                tag.decompose()  # Remove from the tree

        # Extract clean text
        text = target.get_text(separator="\n", strip=True)
        print(text)
    else:
        print("Target section not found.")

if __name__ == "__main__":
    print(scrape_text("https://informer.rs/politika/vesti/1014309/loncar-dincic-zdravstveno-stanje"))