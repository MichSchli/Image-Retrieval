__author__ = 'Michael'
'''
Imports:
'''

import random
import os

'''
Utility functions:
'''

#Define a function to get immediate successor directories:
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

#Define a function to get all jpg files in a folder:
def get_jpg_files(a_dir):
    return [name for name in os.listdir(a_dir) if (os.path.isfile(os.path.join(a_dir, name)) and name.endswith('.jpg'))]

'''
Directory traversal:
'''

#Define a function to recursively build a list of files:
def build_dataset(path):
    items = []

    cat = path.split("/")[-1]

    #Get files in current folder:
    for file in get_jpg_files(path):
        items.append([path + '/'+file, cat, path + '/'+file[:-3]+"sift"])

    #Get files in subfolders:
    for subdir in get_immediate_subdirectories(path):
        items.extend(build_dataset(path + '/'+subdir))

    return items

'''
SIFT parsing:
'''

#Define a function to parse a sift file:
def read_sifts(path):
    sifts = []

    if not os.path.isfile(path):
        return "Error"

    f = open(path)
    for l in f:
        lsplit = l.strip().split(" ")

        if not len(lsplit) == 132:
            return "Error length = "+str(len(lsplit))

        sifts.append([int(x) for x in lsplit[4:]])

    return sifts


'''
Interface
'''

def get_data_list(folder="images"):
    data = build_dataset(folder)

    images = [x[0] for x in data]
    descriptors = [x[2] for x in data]

    return images, descriptors

#Define a function to get a list of image tuples with a list of SIFT descriptors:
def get_image_list(folder="images", limit=None):
    #Build a list of file paths:
    images = build_dataset(folder)

    #Pick a sample if a limit on the number of images is set:
    if limit is not None:
        images = random.sample(images, limit)

    #Load in the corresponding descriptors:
    descriptors = [read_sifts(x[2]) for x in images]

    #Remove the descriptor paths:
    images = [x[0] for x in images]

    #Return the result:
    return images, descriptors

'''
Testing:
'''

if __name__ == '__main__':
    images,descriptors = get_image_list(limit=10)

    print images[0]
    print descriptors[0]


