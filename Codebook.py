__author__ = 'Michael'
'''
Imports:
'''
import ImageLibraryLoader
from sklearn.cluster import KMeans
from itertools import chain
import pickle
import os

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
    kmeans = KMeans(n_clusters=K)

    #Train the algorithm:
    return kmeans.fit(data)

'''
Vector Quantization:
'''

#Define a function to calculate a word histogram from a list of descriptors and a trained clustering:
def get_bag_of_words(descriptors, kmeans):
    if len(descriptors) == 0:
        return {}

    words = kmeans.predict(descriptors)

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

#Evaluates goodness of fit based on mean square error
def evaluate(kmeans, test_samples):
    #Find predictions
    predictions = kmeans.fit_predict(test_samples)

    #Compute (X-mu)^2 for each sample
    for i in xrange(len(predictions)):
        #Calculate error:
        error = test_samples[i] - kmeans.cluster_centers_[predictions[i]]

        #Square the error:
        predictions[i] = error.dot(error)

    #Return the mean:
    return predictions.mean()

#Crossvalidates to test the data on a specific number of clusters:
def cross_validate(test_samples, number_of_clusters, number_of_folds=5):
    #Split into evenly sized chunks:
    samples_per_fold = len(test_samples)/number_of_folds
    folds = [list(t) for t in zip(*[iter(test_samples)]*samples_per_fold)]

    mse = 0

    #Iterate over the folds:
    for i in xrange(number_of_folds):
        print i
        #Get a view of the data:
        train = folds[:]

        #Construct training and test sets:
        test = train.pop(i)
        train = unwrap_descriptor_list(train)

        #Train kmeans:
        kmeans = train_kmeans(train, number_of_clusters)

        #Evaluate mean square error:
        mse += evaluate(kmeans, test)

    #Return the average mean square error over the folds:
    return mse/float(number_of_folds)

'''
Interface:
'''

def construct_full_indexing(kmeans):
    #Defines the update rate:

    images, descriptors = ImageLibraryLoader.get_data_list()
    bows = [get_bag_of_words(ImageLibraryLoader.read_sifts(x), kmeans) for x in descriptors]

    return images, bows


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
    return kmeans, zip(images, bows)

#Define a function to save a codebook to a file:
def save_codebook(codebook, filename):
    pickle.dump(codebook, open( filename, "wb" ) )

#Define a funciton to load a codebook from a file
def load_codebook(filename):
    cb = pickle.load( open(filename, "rb" ) )
    return cb


'''
Testing:
'''

if __name__ == '__main__':
    #Get a bunch of descriptors:
    images, descriptors = ImageLibraryLoader.get_image_list(limit=100)

    #Define a list of K values:
    N_clusters = [1750, 2000, 2250, 2500, 2750, 3000]

    #Define a list of validation scores:
    cv_scores = []

    #Iterate through the list:
    for n in N_clusters:
        print "Testting with", n,"clusters."
        print cross_validate(unwrap_descriptor_list(descriptors), n)