import os
import glob
import sys
import shutil

def main():
    cur_dir = sys.argv[1]
    save_dir = sys.argv[2]
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    sub_folders = os.listdir(cur_dir)
    for sub_folder in sub_folders:
        sub_dir = cur_dir + '/' + sub_folder
        print(sub_dir)
        print(os.path.isdir(sub_dir))
        if(os.path.isdir(sub_dir)):
            save_sub_dir = save_dir + '/' + sub_folder

            if not os.path.exists(save_sub_dir):
                os.mkdir(save_sub_dir)
            img_pathes = glob.glob(sub_dir+'/*.jpg')
            i = 0
            count_img = len(img_pathes)
            while i < count_img:
                save_path = img_pathes[i].replace(sub_dir, save_sub_dir)
                print("move %s to %s"%(img_pathes[i], save_path))
                shutil.copy(img_pathes[i], save_path)
                i += 30

if __name__ == "__main__":
    main()

