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
	return(json.loads(data.decode("utf-8")))

def get_data_from_payload(movie_data, details, prod_companies, prod_countries, genres, movie_detais_headers, movie_id):
	df = json_normalize(movie_data)
	print(df)
	details = details.append(df[movie_detais_headers])

	for movie_genre in df['genres'][0]:
		movie_genre.update({'movie_id': movie_id})
		genres = genres.append(movie_genre, ignore_index=True)

	for countries in df['production_countries'][0]:
		print(countries)
		countries.update({'movie_id': movie_id})
		prod_countries = prod_countries.append(countries, ignore_index=True)

	for companies in df['production_companies'][0]:
		print(companies)
		companies.update({'movie_id': movie_id})
		prod_companies = prod_companies.append(companies, ignore_index=True)

	return details, prod_companies, prod_countries, genres

def get_details_from_payload(movie_data, details, movie_detais_headers, movie_id):
	df = json_normalize(movie_data)
	details = details.append(df[movie_detais_headers])

	return details

def get_details_from_ids(ids, conn, movie_detais_headers):

	details = pd.DataFrame()
	prod_companies = pd.DataFrame()
	prod_countries = pd.DataFrame()
	genres = pd.DataFrame()

	for movie_id in ids:
		#get the data
		url = get_url(movie_id, API_KEY)
		movie_data = get_json(conn, url)
		try:
			details, prod_companies, prod_countries, genres = get_data_from_payload(movie_data, details, prod_companies, prod_countries, genres, movie_detais_headers, movie_id)
		except Exception as e:
			if (movie_data['status_code'] == 25):
				#limit of 40 requests per 10 seconds reached!
				time.sleep(10)
				movie_data = get_json(conn, url)
				details, prod_companies, prod_countries, genres = get_data_from_payload(movie_data, details, prod_companies, prod_countries, genres, movie_detais_headers, movie_id)
	print(genres.head(5))

	details.to_csv('details.csv')
	genres.to_csv('genres.csv')
	prod_companies.to_csv("prod_companies.csv")
	prod_countries.to_csv("prod_countries.csv")


def get_details_only_from_ids(ids, conn, movie_detais_headers):

	details = pd.DataFrame()
	length = len(ids)
	for idx, movie_id in enumerate(ids):
		#get the data
		url = get_url(movie_id, API_KEY)
		movie_data = get_json(conn, url)
		try:
			details = get_details_from_payload(movie_data, details, movie_detais_headers, movie_id)
		except Exception as e:
			if (movie_data['status_code'] == 25):
				#limit of 40 requests per 10 seconds reached!
				print('sleeping')
				time.sleep(10)
				movie_data = get_json(conn, url)
				details = get_details_from_payload(movie_data, details, movie_detais_headers, movie_id)
		print("%s of %s ids" % (idx, length))
		if (idx % 10000 == 0):
			details.to_csv('details_%s.csv' % idx)


def main():
	with open('data/out.csv', 'r') as f:
		reader = csv.reader(f, skipinitialspace=True, delimiter=',')
		ids_list = list(reader)

	ids = [item for sublist in ids_list for item in sublist]

	movie_detais_headers = ['budget', 'id', 'imdb_id', 'original_language', 'original_title', 'release_date', 'revenue', 'runtime', 'vote_average', 'vote_count']

	conn = http.client.HTTPSConnection("api.themoviedb.org")
	#get_details_from_ids(ids, conn, movie_detais_headers)
	get_details_only_from_ids(ids, conn, movie_detais_headers)



if __name__ == "__main__":
    main()
