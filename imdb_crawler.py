from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd


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
	#print(rating)
	#print(rating.text)

def get_rating(soup):
	rating = soup.find("div", {"class" : "imdbRating"})
	rating_value = rating.find("span", {"itemprop" : "ratingValue"}).text
	rating_count  = rating.find("span", {"itemprop" : "ratingCount"}).text
	return rating_value, rating_count


data = pd.read_csv('data/details_us/details.csv')

data.drop(['Unnamed: 0'], axis=1, inplace=True)
print(data.head())

mpaa_rating = []
rating = []
for index, row in data.iterrows():
	print(row['imdb_id'])
	title_id = row['imdb_id']
	soup = get_soup(base_url, row['imdb_id'])

	mpaa = get_MPAA_rating(soup)
	rate, count = get_rating(soup)
	mpaa_rating.append(mpaa)
	rating.append(rate)

mpaa_se = pd.Series(mpaa_rating)
rating_se = pd.Series(rating)

data['MPAA'] = mpaa_se.values
data['rating_imdb'] = rating_se.values
details.to_csv('./data/details_us/details_IMDB.csv')
