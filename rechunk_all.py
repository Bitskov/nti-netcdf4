import os
from netCDF4 import Dataset

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
			for file in get_netcdf_files(path):
				if '.nc' in file:
					files.append(file)
	return files


configurations = [(24, 452, 406), (24, 46, 41), (1, 226, 203), (1, 45, 40)] # chunk sizes (time, y, x)

for file in get_netcdf_files('/'):
	print("Converting file %s" % file[:-2])
	try:
		dataset = Dataset(file)
		os.system("nccopy -d1 %s %s/tmp.nc" % (file, file))
		print("Temprorary copy has been created")
		for configuration in configurations:
			print("Creating file for configuration %s" % str(configuration))
			os.system("nccopy -d1 -c time_counter/%i,y/%i,x/%i %s/tmp.nc %s/data_%i_%i_%i.nc" % (*configuration, file[:-2], file[:-2], *configuration))
			print("File for %s configuration has been created" % str(configuration))
		
		print("Rechunking has been done")
	except IOError:
		print('No such file')
	