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

if __name__ == "__main__":
    print(scrape_politika())