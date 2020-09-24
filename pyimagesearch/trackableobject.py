# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 09:29:20 2020

@author: https://www.pyimagesearch.com/2017/09/18/real-time-object-detection-with-deep-learning-and-opencv/
"""


class TrackableObject:
    def __init__(self, objectID, centroid):
        # store the object ID, then initialize a list of centroids
        # using the current centroid
        self.objectID = objectID
        self.centroids = [centroid]  # ex: [314 295]

        self.start = centroid

        # initialize a boolean used to indicate if the object has
        # already been counted or not
        self.counted = False
