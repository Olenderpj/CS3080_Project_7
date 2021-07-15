""" Author: PJ Olender
    Date Completed: 7/14/2021
    Due Date: 7/17/2021
    Class: CS 3080-Summer 2021
    Github: https://github.com/Olenderpj/CS3080_Project7.git
    Description: Scrape a provided web page (wikipedia) for a table of movie
    information and pull out the gross profit and year of the movie. Using this
    information provide a clean output of gross movie profits by year sorted by
    the year's gross profit from smallest to largest profit
"""


from bs4 import BeautifulSoup
import requests
import re


# Remove non digit characters from a string and return an integer
def convertGrossProfitToInteger(grossProfitAsString):
    grossProfitAsString = filter(str.isdigit, profit)
    grossProfit = int("".join(grossProfitAsString))
    return grossProfit


# Add movie to dictionary, if the movie already exists then add the gross profit
#   to the year's total
def addMovieToDictionary(dictionary, movieYear, movieProfit):
    if movieYear in dictionary.keys():
        totalProfit = dictionary[movieYear]
        totalProfit += movieProfit
        dictionary[movieYear] = totalProfit
    else:
        dictionary[movieYear] = movieProfit


# Use the provided formatting to format the output
def formatAndPrintDictionary(dictionary):
    for year, totalEarnings in dictionary.items():
        print('{:4}    ${:20,}'.format(year, totalEarnings))


# return a dictionary sorted by value
def sortDictionaryByValue(dictionary):
    tempDict = {}
    sortedDictionaryAsArray = sorted(dictionary.items(), key=lambda x: x[1])

    # Tuple unpack the elements of the array
    for element in sortedDictionaryAsArray:
        year, profit = element
        tempDict[year] = profit

    return tempDict


# Ask the user for the URL to use
print("What url do you want to explore?")
url = input()
response = requests.get(url)

# Parse the Html file for the specific table from the saved wikipedia HTML
soup = BeautifulSoup(response.text, 'html.parser')
tableRows = soup.find("table", {"class": "wikitable sortable plainrowheaders"})
movies = tableRows.find_all("tr")

movieInformation = {}

# Use the data from the parsed table to find the year and gross profit of each movie
for movie in movies:
    grossProfit = movie.find_all("td", {"align": "right"})
    years = movie.find_all("td", {"style": "text-align:center;"})

    # Use regex to pull out the year and gross profit from each HTML Tag
    for profit, year in zip(grossProfit, years):
        profit = re.search("\\$(?P<grossProfit>[0-9,]+)", profit.text)
        year = re.search("(?P<year>[0-9]{4})", str(year.text))

        profit = profit.group("grossProfit")
        movieYear = int(year.group("year"))
        movieProfit = convertGrossProfitToInteger(profit)

        # Append to the dictionary both year and gross profit for each movie
        if year is not None and profit is not None:
            addMovieToDictionary(movieInformation, movieYear, movieProfit)

# Sort the dictionary and print with formatting
movieInformation = sortDictionaryByValue(movieInformation)
formatAndPrintDictionary(movieInformation)
