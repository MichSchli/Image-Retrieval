__author__ = 'Michael'
'''
Imports:
'''
import ImageLibraryLoader
from sklearn.cluster import KMeans
from itertools import chain

'''
Utility functions:
'''

#Define a function to unwrap a list of descriptors for processing:
def unwrap_descriptor_list(descs):
    return list(chain.from_iterable(descs))

'''
Clustering:
'''

#Define a function to train a kmeans clustering algorithm on the data:
def train_kmeans(data, K):
    #Create Kmeans object:
    kmeans=KMeans(n_clusters=K)

    #Train the algorithm:
    return kmeans.fit(data)

'''
Vector Quantization:
'''

#Define a function to calculate a word histogram from a list of descriptors and a trained clustering:
def get_bag_of_words(descriptors, kmeans):
    words = kmeans.fit_predict(descriptors)

    h = {}

    for w in words:
        if w in h.keys():
            h[w] += 1
        else:
            h[w] = 1

    return h

#Define a function to calculate a list of bag-of-words representations:
def calculate_bags_of_words(descriptors, kmeans):
    bow = []
    for i in xrange(len(descriptors)):
        bow.append(get_bag_of_words(descriptors[i], kmeans))

    return bow

'''
Evaluation:
'''

'''
Interface:
'''

#Define a function to construct table of image/bag-of-words pairs:
def construct_table(K, limit=None):
    images, descriptors = ImageLibraryLoader.get_image_list(limit=limit)

    if len(images) != len(descriptors):
        return "Error"

    #Train a kmeans clustering:
    kmeans = train_kmeans(unwrap_descriptor_list(descriptors), K)

    #Calculate the bags of words:
    bows = calculate_bags_of_words(descriptors, kmeans)

    #Zip the lists together:
    return zip(images, bows)

'''
Testing:
'''

if __name__ == '__main__':
    print construct_table(10, limit=4)