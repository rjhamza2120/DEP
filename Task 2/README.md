# IMDb Web Scraper

This project is a Python-based web scraper designed to extract data from the IMDb Top Movies list. The script retrieves information such as movie rankings, titles, release years, and IMDb ratings, and stores the data in a CSV file for easy analysis.


## Script Overview:

Here's a breakdown of the script:

>>#### • Imports:
>>>The script begins by importing the necessary libraries: requests, BeautifulSoup, and pandas.

>>#### • Initialization:
>>>A CSV file named Scraped.csv is created with columns: Rating, Movie Name, Year, IMDb Rating.

>>#### • Request to IMDb:
>>>The script sends an HTTP GET request to the IMDb Top movies page using the requests library.

>>#### • Parsing HTML:
>>>The HTML content of the page is parsed using BeautifulSoup.

>>#### • Data Extraction:
>>>The script extracts the relevant data (movie rank, name, year, and rating) from the parsed HTML.

>>#### • Saving Data:
>>>The extracted data is appended to the Scraped.csv file.

>>#### • Error Handling:
>>>A try-except block is used to handle any potential errors during the web scraping process.


## Features:

>>#### • Fetch IMDb Top Movies:
>>> The script scrapes the IMDb website for the movies based on user ratings.

>>#### • Data Extraction:
>>> It extracts the ranking, movie name, release year, and IMDb rating for each movie.

>>#### • CSV Output:
>>> The extracted data is saved in a CSV file named Scraped.csv.

>>#### >• Error Handling:
>>> The script includes basic error handling to manage potential issues during the web scraping process.


## Requirements:

Before running the script, ensure you have the following Python libraries installed:

>>#### • requests:
>>> To send HTTP requests to the IMDb website.

>>#### • beautifulsoup4:
>>> To parse and navigate the HTML content of the webpage.

>>#### • pandas:
>>> To manage and save the extracted data into a CSV file.
