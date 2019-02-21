# Package
import os
import json
import shutil

###############################################################################
# Input
basedir = "/Users/pierre_pc/Desktop"
task = 'shenzhen_0111_1_withlight'
#pkgsize = 120
pkgsize = 50
###############################################################################

savedir = os.path.join(basedir, 'temp_storage', task)
taskdir = os.path.join(basedir, task)

filelist = []
def gci(filepath):
	files = os.listdir(filepath)
	for fi in files:
		fi_d = os.path.join(filepath, fi)
		if os.path.isdir(fi_d):
			gci(fi_d)
		else:
			if os.path.splitext(fi_d)[1] == '.jpg':
				filelist.append(os.path.join(filepath,fi_d))
gci(taskdir)
filelist.sort()

indx = 1
foldernum = 1
for imoldpath in filelist:
	if indx > pkgsize:
		indx = 1
		foldernum += 1

	# Make a folder
	subfolder = os.path.join(savedir, 'part_{:03}'.format(foldernum))
	if not os.path.exists(subfolder):
		os.makedirs(subfolder)

	# Move files
	shutil.copy2(imoldpath, subfolder)
	print(imoldpath)

	indx += 1

print('All Finished')




