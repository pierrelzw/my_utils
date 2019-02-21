import os
import random
import scipy.misc as m
import math
from multiprocessing import Pool
import shutil

###############################################################################
# Input
basedir = '/Users/pierre_pc/Desktop/temp_storage/'
dataset = '20190116_segment_city_1309'
###############################################################################

worker_num = 4
savedir = basedir+'temp_marked/'+dataset
basedir = basedir + dataset

def gci(filepath):
    def __gci(filepath):
        files = os.listdir(filepath)
        for fi in files:
            fi_d = os.path.join(filepath, fi)
            if os.path.isdir(fi_d):
                __gci(fi_d)
            else:
                if os.path.splitext(fi_d)[1] == '.jpg':
                    file_list.append(os.path.join(filepath,fi_d))

    file_list = []
    __gci(filepath)
    return file_list

def son_process_watermark(name, img1, img2, impath, transparency):
	print('Process %s is running'%name)
	imdir = os.path.dirname(impath)
	imname = os.path.basename(impath)

	if os.path.splitext(imname)[1] == '.jpg':
		imsavedir = imdir.replace(basedir, savedir)

		if not os.path.exists(imsavedir):
			os.makedirs(imsavedir)

		img = m.imread(impath)

		# Random position
		rb = random.randint(0, img.shape[0]-img1.shape[0])
		cb = random.randint(0, img.shape[1]-img1.shape[1])
		re = rb+img1.shape[0]
		ce = cb+img1.shape[1]
		img[rb:re,cb:ce,:] = transparency*img[rb:re,cb:ce,:]+ (1-transparency)*img1

		rb = random.randint(0, img.shape[0]-img2.shape[0])
		cb = random.randint(0, img.shape[1]-img2.shape[1])
		re = rb+img2.shape[0]
		ce = cb+img2.shape[1]
		img[rb:re,cb:ce,:] = transparency*img[rb:re,cb:ce,:]+ (1-transparency)*img2

		m.imsave(imsavedir+'/'+imname, img)

def son_process_compress(savedir):
	os.system('7z a -pautolab '+savedir+'.7z '+savedir)
	os.system('rm -r '+savedir)

# Imname list
filelist = gci(basedir)
filelist.sort()

# Mark settings
img1 = m.imread('./logos/tencent_logo.jpg')
img2 = m.imread('./logos/tencent_map.jpg')[:,:,0:3]
mark_height = 60.0
transparency = 0.90
ratio = mark_height / img1.shape[0]
img1 = m.imresize(img1, (math.floor(img1.shape[0]*ratio),math.floor(img1.shape[1]*ratio)))
img2 = m.imresize(img2, (80,80))

# Main process
# Step 1 Watermark
pool = Pool(worker_num)
for i, impath in enumerate(filelist):
	pool.apply_async(son_process_watermark, args=('son_%d'%i, img1, img2, impath, transparency))
pool.close()
pool.join()

# Step 2 Compress
pool = Pool(worker_num)
for subdir in os.listdir(savedir):
	pool.apply_async(son_process_compress, args=(savedir+'/'+subdir,))
pool.close()
pool.join()
print(dataset+' Finished')

