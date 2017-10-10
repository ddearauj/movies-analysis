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

with open('out.csv', 'r') as f:
	reader = csv.reader(f, skipinitialspace=True, delimiter=',')
	ids_list = list(reader)

ids = [item for sublist in ids_list for item in sublist]

conn = http.client.HTTPSConnection("api.themoviedb.org")
for movie_id in ids[:3]:
	url = get_url(movie_id, API_KEY)
	movie_data = get_json(conn, url)
	df = json_normalize(movie_data)
	print(df.head(5))