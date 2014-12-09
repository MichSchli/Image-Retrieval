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
    kmeans = KMeans(n_clusters=K)

    #Train the algorithm:
    return kmeans.fit(data)

'''
Vector Quantization:
'''

#Define a function to calculate a word histogram from a list of descriptors and a trained clustering:
def get_bag_of_words(descriptors, kmeans):
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

    images, descriptors = ImageLibraryLoader.get_image_list(limit=4)

    #print cross_validate(unwrap_descriptor_list(descriptors), 10)
    #t = train_kmeans(unwrap_descriptor_list(descriptors), 10)

    #print evaluate(t, unwrap_descriptor_list(descriptors))

    print construct_table(10, limit=4)