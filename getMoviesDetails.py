import http.client
import json
from settings import API_KEY
import time
import  csv
from pandas.io.json import json_normalize
import pandas as pd

def get_url(movie_id, api_key):
	return("/3/movie/" + str(movie_id) + "?api_key=" + str(api_key))

def get_json(conn, url):
	payload = "{}"
	conn.request("GET", url, payload)
	res = conn.getresponse()
	data = res.read()
	header = res.getheader("Retry-After")
	if header:
		header = int(header)
	return(json.loads(data.decode("utf-8")), header)

def get_data_from_payload(movie_data, details, prod_companies, prod_countries, genres, movie_detais_headers, movie_id):
	""" since the movie_data has JSON files in their rows, we break them into seperate DataFrames """
	df = json_normalize(movie_data)
	#print(df)
	#print(details.head())
	details = details.append(df[movie_detais_headers])

	for movie_genre in df['genres'][0]:
		movie_genre.update({'movie_id': movie_id})
		genres = genres.append(movie_genre, ignore_index=True)

	for countries in df['production_countries'][0]:
		#print(countries)
		countries.update({'movie_id': movie_id})
		prod_countries = prod_countries.append(countries, ignore_index=True)

	for companies in df['production_companies'][0]:
		#print(companies)
		companies.update({'movie_id': movie_id})
		prod_companies = prod_companies.append(companies, ignore_index=True)

	return details, prod_companies, prod_countries, genres

def get_details_from_ids(ids, conn, movie_detais_headers):

	details = pd.DataFrame()
	prod_companies = pd.DataFrame()
	prod_countries = pd.DataFrame()
	genres = pd.DataFrame()
	length = len(ids)

	for idx, movie_id in enumerate(ids):
		#get the data
		url = get_url(movie_id, API_KEY)
		movie_data, header = get_json(conn, url)
		#print(movie_data)

		if ('status_code' in movie_data):
			#limit of 40 requests per 10 seconds reached!
			print(header)
			time.sleep(header + 1)
			movie_data, header = get_json(conn, url)
			details, prod_companies, prod_countries, genres = get_data_from_payload(movie_data, details, prod_companies, prod_countries, genres, movie_detais_headers, movie_id)
		else:
			details, prod_companies, prod_countries, genres = get_data_from_payload(movie_data, details, prod_companies, prod_countries, genres, movie_detais_headers, movie_id)

		print("%s of %s ids" % (idx, length))

	#print(genres.head(5))

	details.to_csv('data/us/details.csv')
	genres.to_csv('data/us/genres.csv')
	prod_companies.to_csv("data/us/prod_companies.csv")
	prod_countries.to_csv("data/us/prod_countries.csv")

def main():
	with open('data/us/out.csv', 'r') as f:
		reader = csv.reader(f, skipinitialspace=True, delimiter=',')
		ids_list = list(reader)

	ids = [item for sublist in ids_list for item in sublist]
	print(len(ids))

	movie_detais_headers = ['budget', 'id', 'imdb_id', 'original_language', 'original_title', 'release_date', 'revenue', 'runtime', 'vote_average', 'vote_count']

	conn = http.client.HTTPSConnection("api.themoviedb.org")
	#get_details_from_ids(ids, conn, movie_detais_headers)
	get_details_from_ids(ids, conn, movie_detais_headers)



if __name__ == "__main__":
    main()
