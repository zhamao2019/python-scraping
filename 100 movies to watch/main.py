import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(url=URL)
web_html = response.text

soup = BeautifulSoup(web_html, "html.parser")
all_movies = soup.find_all(name="h3", class_="title")

all_movies_titles = [movie.getText() for movie in all_movies]
print(all_movies_titles[::-1])
with open("movies.txt", mode="w") as file:
    for movie in all_movies_titles[::-1]:
        file.write(f"{movie}\n")
