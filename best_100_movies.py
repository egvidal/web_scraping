import requests
from bs4 import BeautifulSoup

URL = "https://www.imdb.com/list/ls055592025/"
response = requests.get(URL)
content = response.text

soup = BeautifulSoup(content, "html.parser")

# print(soup.find_all(name="h3", class_="lister-item-header"))
all_movies = soup.select(selector=".lister-item-header a")
titles_list = [f"{all_movies.index(movie) + 1}. {movie.getText()}" for movie in all_movies]
# print(titles_list)

all_years = soup.select(selector=".lister-item-year")
years_list = [year.getText() for year in all_years]
# print(years_list)

for i in range(len(titles_list)):
  titles_list[i] = titles_list[i] + " " + years_list[i]

print(titles_list)

file = open("./best_100_movies.txt", "wt")
for title in titles_list:
  file.write(f"{title}\n")
file.close()
