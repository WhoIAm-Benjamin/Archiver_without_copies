import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename=r'logs.log',
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    filemode='w'
                    )


unavaliable = [] # ['AVI', 'avi']
avaliable_files = []
files = []

def walk(directory):
	files_in_directory = os.listdir(directory)
	for l in files_in_directory:
		local_path = os.path.join(directory, l)
		if os.path.isdir(local_path) is True:
			walk(local_path)
		else:
			splitting = l.split('.')
			if splitting[-1] not in unavaliable:
				avaliable_files.append(l)

def comparison(file_1, file_2):
	if file_1 == file_2:
		logging.debug('file_1 == file_2')
		return True
	return False

sources = input('Enter sources with ",": ').replace('/', '\\').strip().split(',')
for i in sources:
	if os.path.exists(i.strip()) is False:
		del sources[sources.index(i)]
target_dir = input('Enter folder for archiving: ').replace('/', '\\')

print('Working...')
for folder in sources:
	walk(folder.strip())
	i = 0
	try:
		while True:
			path_0 = os.path.join(folder, avaliable_files[i])
			logging.debug(path_0)
			try:
				if os.path.exists(path_0):
					with open(path_0, 'rb') as f:
						content_1 = f.read()
					if len(avaliable_files) == 1:
						files.append(path_0)
						del avaliable_files[0]
						logging.debug('One file')
						break
				else:
					i += 1
					continue
				while True:
					try:
						path = os.path.join(folder, avaliable_files[i+1])
						with open(path, 'rb') as f:
							content_2 = f.read()
						result = comparison(content_1, content_2)
						if result:
							os.remove(path)
							print('File {} deleted'.format(os.path.basename(path)))
						i += 1
					except IndexError:
						files.append(path_0)
						del avaliable_files[0]
						print('File {} appended'.format(os.path.basename(path_0)))
						i = 0
						break
					except FileNotFoundError:
						logging.debug('FileNotFoundError')
						i += 1
						del avaliable_files[i]
						continue
					except MemoryError:
						logging.debug('MemoryError(into)')
						del avaliable_files[i]
						files.append(path_0)
			except MemoryError:
				logging.debug('MemoryError')
				del avaliable_files[i]
				files.append(path_0)
				continue
			except IndexError:
				logging.debug('Except IndexError(into)')
				break
	except IndexError:
		logging.debug('Except IndexError')
		pass
	finally:
		logging.debug('Work is successfull')
		print('End of work comparision')

zip_command = "zip -qr {0} -i {1}".format(target_dir, ' '.join(files))
if os.system(zip_command) == 0:
	print('Reserve copies was successfull added in', target_dir)
else:
	print('Reserve copied wasn\'t added')
