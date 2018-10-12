import os
def create_dir(cur_path):
    while not os.path.exists(os.path.dirname(cur_path)):
        create_dir(os.path.dirname(cur_path))
    os.mkdir(cur_path)

