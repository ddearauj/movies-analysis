from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

base_url = 'http://www.imdb.com/title/'
#title_id = 'tt0144084'
title_id = 'tt1345836'

url = base_url + title_id

def get_soup(base_url, title_id):

	req = Request(
		url, 
		data=None, 
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		}
	)

	soup = BeautifulSoup(urlopen(req), "lxml")
	return soup

def get_MPAA_rating(soup):
	storyline = soup.find("div", {"id" : "titleStoryLine"})
	rating = storyline.find("span", {"itemprop" : "contentRating"})
	print(rating)
	print(rating.text)

def get_rating(soup):
	rating = soup.find("div", {"class" : "imdbRating"})
	rating_value = rating.find("span", {"itemprop" : "ratingValue"}).text
	rating_count  = rating.find("span", {"itemprop" : "ratingCount"}).text
	return rating_value, rating_count



print(get_rating(get_soup(base_url, title_id)))