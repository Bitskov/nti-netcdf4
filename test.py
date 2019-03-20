from netCDF4 import Dataset
import time
import os
import pickle
from random import randint

def get_netcdf_files(dir):
	root_dir = dir
	files = []
	content = os.listdir(dir)
	for f in content:
		path = os.path.join(root_dir, f)
		if os.path.isfile(path):
			if'.nc' in path:
				files.append(path)
		if os.path.isdir(path):
			for file in get_books_files(path):
				if '.nc' in file:
					files.append(file)
	return files

def get_map(ds, param):
	start = time.time()
	a = randint(0, 23)
	b = randint(0, 23)
	if param == 'sossheig':
		result = ds.variables[param][min(a,b):max(a,b)]
	if param == 'vosaline' or param == 'votemper':
		result = ds.variables[param][randint(0, 17)][min(a,b):max(a,b)]
	end = time.time()
	return result, end - start
	
def get_series(ds, param):
	start = time.time()
	a = randint(0, 11)
	b = randint(12, 23)
	x = randint(0, 405)
	y = randint(0, 451)
	time_range = range(min(a, b), max(a, b))
	if param == 'sossheig':
		for t in time_range:
			result = ds.variables[param][t][y][x]
	if param == 'vosaline' or param == 'votemper':
		depth = randint(0, 17)
		for t in time_range:
			result = ds.variables[param][t][depth][y][x]
	end = time.time()
	return result, end - start
	

path = input()
N = int(input())

print(get_netcdf_files(path + '/'))

for file in get_netcdf_files(path + '/'):
	if 'data' not in file:
		continue
		
	dataset = Dataset(file)
	
	t_series = 0
	t_maps = 0
	
	series_time = []
	maps_time = []
	sums = []
	
	params = ['sossheig', 'vosaline', 'votemper']
	
	for _ in range(N):
		if (N % 10 == 0):
			print(N)
		_, t_ser = get_series(dataset, params[randint(0, 2)])
		_, t_map = get_map(dataset, params[randint(0, 2)])
		t_series += t_ser
		t_maps += t_map
		
		series_time.append(t_ser)
		maps_time.append(t_map)
		sums.append(t_ser + t_map)
		
	all_time = sum(sums)
	
	print('Series times %s' % str(series_time))
	print('Maps times %s' % str(maps_time))
	
	print('Configuration %s has taken %f secons' % (str(dataset.variables['sossheig'].chunking()), all_time))
	
	print('Median time %f' % sorted(sums)[len(sums) // 2])
	print('Average time %f' % (sum(sums) / len(sums)))
	
	data = {}
	data['Configuration'] = list(dataset.variables['sossheig'].chunking())
	data['N'] = N
	data['Average time'] = sum(sums) / len(sums)
	data['Median time'] = sorted(sums)[len(sums) // 2]
	data['All time'] = all_time
	data['Maps time'] = maps_time
	data['Series time'] = series_time
	data['2 queries time'] = sums
		
	with open('%s/%s%s.pkl' % (path, str(dataset.variables['sossheig'].chunking()), path), 'wb') as f:
		pickle.dump(data, f)
	
	print("All data has been saved to %s.pkl" % str(dataset.variables['sossheig'].chunking()))