__author__ = 'Michael'
'''
Imports:
'''

from skimage.feature import daisy
from skimage.io import ImageCollection
from skimage.io import imread
from skimage.viewer import ImageViewer
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
        items.extend(build_dataset( path + '/'+subdir))

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

#Define a function to get a list of image tuples with a list of SIFT descriptors:
def get_image_list(folder="images"):
    #Build a list of file paths:
    images = build_dataset(folder)

    #Load in the corresponding descriptors:
    descriptors = [read_sifts(x[2]) for x in images]

    #Remove the descriptor paths:
    images = [x[:1] for x in images]

    #Return the result:
    return images, descriptors

'''
Testing:
'''

if __name__ == '__main__':
    images,descriptors = get_image_list()

    print images[0]
    print descriptors[0]


