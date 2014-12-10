__author__ = 'Michael'
'''
Imports:
'''
import Codebook
import math
from skimage.viewer import ImageViewer
from skimage.io import imread
'''
Image matching algorithm:
'''

#Define a function to find the best match for an image given a metric
def find_best_match(image_index, bow_list, metric):
    best = -1
    best_distance = None

    #Iterate over all possible matches:
    for i in xrange(len(bow_list)):
        #Don't match an image to itself:
        if image_index != i:
            #Calculate the distance:
            d = metric(bow_list[image_index], bow_list[i])

            #If the new distance is better, memorize it:
            if best_distance == None or best_distance > d:
                best = i
                best_distance = d

    #Return the best match:
    return best

'''
Metrics:
'''

#Calculate the number of common words:
def common_words(bow1, bow2):
    ks1 = set(bow1.keys())
    ks2 = set(bow2.keys())
    return -len(ks1.intersection(ks2))

#Kullback-Leibler distance:
def symmetric_kullback_leibler(bow1, bow2):
    kbsum = 0
    for i in bow1.keys():
        if i not in bow2.keys():
            continue
        kbsum += bow1[i]*math.log(bow1[i]/float(bow2[i]))

    for i in bow2.keys():
        if i not in bow1.keys():
            continue
        kbsum += bow2[i]*math.log(bow2[i]/float(bow1[i]))

    return kbsum/2.0

#Bhattacharyya distance:
def bhattacharyya_distance(bow1, bow2):
    ks1 = set(bow1.keys())
    ks2 = set(bow2.keys())
    s = 0

    for i in ks1.intersection(ks2):
        s += math.sqrt(bow1[i]*bow2[i])

    return -math.log(s)

#Euclidean distance:
def euclidean_distance(bow1, bow2):
    ks1 = set(bow1.keys())
    ks2 = set(bow2.keys())

    s = 0

    for i in ks1.union(ks2):
        p1 = 0 if i not in ks1 else bow1[i]
        p2 = 0 if i not in ks2 else bow2[i]

        s += (p1-p2)**2

    return math.sqrt(s)

'''
Interface:
'''

def show_best_match(image_id, codebook, metric):
    bows = [x[1] for x in codebook]

    if metric == 'euclidean':
        m = euclidean_distance
    elif metric == 'kullback-leibler':
        m = symmetric_kullback_leibler
    elif metric == 'bhattacharyya':
        m = bhattacharyya_distance
    elif metric == 'common words':
        m = common_words
    else:
        return "Error"

    best_match_path = codebook[find_best_match(image_id, bows, m)][0]

    img = imread(best_match_path)
    view = ImageViewer(img)
    view.show()


'''
Testing:
'''

if __name__ == '__main__':
    #cb = Codebook.construct_table(1000, limit=50)
    #Codebook.save_codebook(cb, "codebook_1000_50.cb")
    cb = Codebook.load_codebook("codebook_1000_50.cb")

    img = imread(cb[0][0])
    view = ImageViewer(img)
    view.show()

    show_best_match(0, cb, 'kullback-leibler')
