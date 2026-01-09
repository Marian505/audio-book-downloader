import httpx
from bs4 import BeautifulSoup
import os

def main():
    print("Audio books downloader run.")
    search_phrase = "human+universe"
    url = "https://appaudiobooks.net"
    get_all = True

    response = httpx.get("https://appaudiobooks.net", params={"s": search_phrase})
    soup = BeautifulSoup(response.text, "lxml")
    articles = soup.find_all("article", class_="post")
    print(f"Atricles count: {len(articles)}.")

    os.makedirs("./data", exist_ok=True)
    for i, article in enumerate(articles if get_all else articles[:1]):
        audios = article.find_all("audio", class_="wp-audio-shortcode")
        print(f"Atricle {i} tracks count: {len(audios)}.")
        os.makedirs(f"./data/article{i}", exist_ok=True)
        for j, audio in enumerate(audios):
            url = audio.select("a[href]")[0].get("href")
            res = httpx.get(url)
            with open(f"./data/article{i}/track{j}.mp3", "wb") as f:
                f.write(res.content)
    print("Audio books downloaded and saved!")

if __name__ == "__main__":
    main()
