import os
from netCDF4 import Dataset

configurations = [(24, 452, 406), (24, 46, 41), (1, 226, 203), (1, 45, 40)] # chunk sizes (time, y, x)

file = input()

try:
	dataset = Dataset(file)
	os.system("nccopy -d1 %s tmp.nc" % file)
	print("Temprorary copy has been created")
	for configuration in configurations:
		print("Creating file for configuration %s" % str(configuration))
		os.system("nccopy -d1 -c time_counter/%i,y/%i,x/%i tmp.nc data_%i_%i_%i.nc" % (*configuration, *configuration))
		print("File for %s configuration has been created" % str(configuration))
		
	print("Rechunking has been done")
except IOError:
	print('No such file')
	
