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

def get_map(ds, param, t, depth=0):
	start = time.time()
	if param == 'vomecrty':
		result = ds.variables[param][t]
	else:
		result = ds.variables[param][t][depth]
	end = time.time()
	return result, end - start
	
def get_series(ds, param, x, y, depth=0):
	start = time.time()
	if param == 'vomecrty':
		for t in range(24):
			result = ds.variables[param][t][depth][x][y]
	else:
		result = ds.variables[param][:][depth][x][y]
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
	
	for _ in range(N):
		if (N % 10 == 0):
			print(N)
		_, t_ser = get_series(dataset, 'vomecrty', randint(0, 451), randint(0, 405))
		_, t_map = get_map(dataset, 'vomecrty', randint(0, 23))
		t_series += t_ser
		t_maps += t_map
		
		series_time.append(t_ser)
		maps_time.append(t_map)
		sums.append(t_ser + t_map)
		
	all_time = sum(sums)
	
	print('Series times %s' % str(series_time))
	print('Maps times %s' % str(maps_time))
	
	print('Configuration %s has taken %f secons' % (str(dataset.variables['vomecrty'].chunking()), all_time))
	
	print('Median time %f' % sorted(sums)[len(sums) // 2])
	print('Average time %f' % (sum(sums) / len(sums)))
	
	data = {}
	data['Configuration'] = list(dataset.variables['vomecrty'].chunking())
	data['N'] = N
	data['Average time'] = sum(sums) / len(sums)
	data['Median time'] = sorted(sums)[len(sums) // 2]
	data['All time'] = all_time
	data['Maps time'] = maps_time
	data['Series time'] = series_time
	data['2 queries time'] = sums
		
	with open('%s/%s%s.pkl' % (path, str(dataset.variables['vomecrty'].chunking()), path), 'wb') as f:
		pickle.dump(data, f)
	
	print("All data has been saved to %s.pkl" % str(dataset.variables['vomecrty'].chunking()))