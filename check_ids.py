import pandas as pd
import numpy as np
import csv
import collections

def get_ids_appended():
	details_ids_list = pd.read_csv('data/details_appending/details_150000.csv')
	details_ids = list(details_ids_list['id'])
	print(details_ids[:5])

	with open('data/out.csv', 'r') as f:
		reader = csv.reader(f, skipinitialspace=True, delimiter=',')
		ids_list = list(reader)

	ids = [item for sublist in ids_list for item in sublist]
	print(ids[:5])

	print(len(pd.Series(details_ids)[pd.Series(details_ids).duplicated()].values))
	print(len(pd.Series(ids)[pd.Series(ids).duplicated()].values))

	main_list = np.setdiff1d(ids, details_ids)
	print(len(main_list))

get_ids_appended()