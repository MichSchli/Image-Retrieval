__author__ = 'Michael'
'''
Imports:
'''
import Codebook

'''
Image matching algorithm:
'''

#Define a function to find the best match for an image given a metric
def find_best_match(image_index, bow_list, metric):
    best = -1
    best_distance = -1

    #Iterate over all possible matches:
    for i in xrange(len(bow_list)):
        #Don't match an image to itself:
        if image_index != i:
            #Calculate the distance:
            d = metric(bow_list[image_index], bow_list[i])

            #If the new distance is better, memorize it:
            if best_distance == -1 or best_distance > d:
                best = i
                best_distance = d

    #Return the best match:
    return best

'''
Interface:
'''

'''
Testing:
'''

if __name__ == '__main__':
    cb = Codebook.construct_table(10, limit=4)

    bows = [x[1] for x in cb]

    img = 0

    print find_best_match(img, bows, lambda x,y: 1)