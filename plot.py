import pickle
import matplotlib.pyplot as plt
import os
import numpy as np

def get_pkl_files(dir):
	root_dir = dir
	files = []
	content = os.listdir(dir)
	for f in content:
		path = os.path.join(root_dir, f)
		if os.path.isfile(path):
			if'.pkl' in path:
				files.append(path)
		if os.path.isdir(path):
			for file in get_books_files(path):
				if '.pkl' in file:
					files.append(file)
	return files
	

path = input()

files = get_pkl_files('%s/' % path)
n = len(files)
fig, ax_lst = plt.subplots(3, figsize=(10, 10))

ax_lst[0].set_title("Maps time")
ax_lst[1].set_title("Series time")
ax_lst[2].set_title("2 queries time")

print('-----------------------------------------------')

for i in range(n):
	file = files[i]

	data = {}
	with open(file, 'rb') as f:
		data = pickle.load(f)
	
	ax_lst[0].plot(np.array([i for i in range(data['N'])]), np.array(data['Maps time']), label=str(data['Configuration']))
	ax_lst[1].plot(np.array([i for i in range(data['N'])]), np.array(data['Series time']), label=str(data['Configuration']))
	ax_lst[2].plot(np.array([i for i in range(data['N'])]), np.array(data['2 queries time']), label=str(data['Configuration']))
	
	for key, value in data.items():
		print(key, value)
	print('-----------------------------------------------')
	
plt.legend()
plt.savefig("%s.png" % path)
plt.show()
	
print('That\'s all information')
