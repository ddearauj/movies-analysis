import http.client
import json
from settings import API_KEY
import time
import  csv

def get_url(year, page, api_key):
	return("/3/discover/movie?primary_release_year=" + str(year) + "&page=" + str(page) + "&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key=" + str(api_key))

def get_json(conn, url):
	payload = "{}"
	conn.request("GET", url, payload)
	res = conn.getresponse()
	data = res.read()
	return(json.loads(data.decode("utf-8")))

def append_movies_from_payload(payload, ids):
	for mydictionary in payload['results']:
		for key in mydictionary:
			#print ("key: %s , value: %s" % (key, mydictionary[key]))
			if key == "id":
				ids.append(mydictionary[key])

def get_movies_from_year(year, conn, api_key):
	# get number of pages
	url = get_url(year, 1, api_key)
	d = get_json(conn, url)
	total_pages = (d['total_pages'])

	# get movies ids
	ids = []
	append_movies_from_payload(d, ids)

	for i in range(2, total_pages + 1):
		print("page: %s " % i)
		url = get_url(year, i, api_key)
		d = get_json(conn, url)


		# for key in d:
		# 	print ("key: %s" % (key))

		try:
			append_movies_from_payload(d, ids)
		except Exception as e:
			print(d['status_code'])
			if (d['status_code'] == 25):
				#limit of 40 requests per 10 seconds reached!
				time.sleep(10)
				d = get_json(conn, url)
				append_movies_from_payload(d, ids)


	print(len(ids))
	return(ids)


	#for i in range(page, total_pages + 1)
	#	url = get_url(year, i, api_key)

def get_movies_from_y0_yf(year_init, year_end, conn):
	""" Get a list of movies from the interval [year_init, year_end] """
	movie_ids = []
	for year in range(year_init, year_end + 1):
		movie_ids.append(get_movies_from_year(year, conn, API_KEY))
	#print(movie_ids)
	print((movie_ids))
	with open('movie_ids.json', 'wb') as outfile:
		json.dumps(movie_ids, outfile)

	with open("out.csv","w") as f:
		wr = csv.writer(f,delimiter="\n")
		wr.writerow(movie_ids)

def main():
	conn = http.client.HTTPSConnection("api.themoviedb.org")
	get_movies_from_y0_yf(2000, 2016, conn)


if __name__ == "__main__":
    main()