from bs4 import BeautifulSoup
import requests
import re

# Ask the user for the URL to use
print("What url do you want to explore?")
#url = input()
url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')


movieData = soup.find_all("td")

for movie in movieData:
    if movie.has_attr("align"):
        print(movie.text)
        td_name = soup.find('td', {"data-sortval":hero})


# Use the following formatting for each year's data
# Print them in increasing order of earnings
#print('{:4}    ${:20,}'.format(year, totalEarnings))