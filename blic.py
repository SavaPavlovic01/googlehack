
import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    ret = [] 
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    titles = soup.find_all('div', {'class': 'news__content'})

    for title in titles:
        ret.append(title.a.get_text())
    return ret

def scrape_politika():
    url_base = "https://www.blic.rs/vesti/politika?strana=" 
    informer_titles = []
    # 17 jer toliko ima :(
    for i in range(34):
        cur_url = url_base + str(i)
        informer_titles += scrape_page(cur_url)

    return informer_titles


if __name__ == "__main__":
    #strana moze do 34
    print(scrape_page("https://www.blic.rs/vesti/politika?strana=3"))