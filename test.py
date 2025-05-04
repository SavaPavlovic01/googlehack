
def get_username_twitter(url):
    username =url.split("x.com/")[1].split('/')[0]
    return username
if __name__ == "__main__":
    print(get_username_twitter("https://x.com/MrKimmKE/status/1918582688979493122"))