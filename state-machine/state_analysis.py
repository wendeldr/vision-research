import os, sys, inspect, io, pickle
import matplotlib.pyplot as plt
from math import floor
import keypoint_helpers
import state_helpers
from scipy.interpolate import spline
import numpy as np
import copy

with open('test.pickle', 'rb') as handle:
    kpts = pickle.load(handle)

kpts_inverted = state_helpers.invert_keypoints(kpts)

keypoints = keypoint_helpers.get_keypoint_labels()
kpt_dict_x = {
    'nose': [],
    'left_eye': [],
    'right_eye': [],
    'left_ear': [],
    'right_ear': [],
    'left_shoulder': [],
    'right_shoulder': [],
    'left_elbow': [],
    'right_elbow': [],
    'left_wrist': [],
    'right_wrist': [],
    'left_hip': [],
    'right_hip': [],
    'left_knee': [],
    'right_knee': [],
    'left_ankle': [],
    'right_ankle': []
}

kpt_dict_y = copy.deepcopy(kpt_dict_x)

time = list(range(len(kpts_inverted)))

for frame in kpts_inverted:
    for i, point in enumerate(frame):
        kpt_dict_x[keypoints[i]].append(point[0])
        kpt_dict_y[keypoints[i]].append(point[1])

# displacement
displacement = {}
for i, kpt in enumerate(keypoints):
    xsquared = np.square(np.asarray(kpt_dict_x[kpt]))
    ysquared = np.square(np.asarray(kpt_dict_y[kpt]))
    displacement[kpt] = np.sqrt(xsquared + ysquared)



velocity = {}
acceleration = {}
for i, kpt in enumerate(keypoints):
    velocity[kpt] = np.diff(displacement[kpt])/np.diff(time)
    acceleration[kpt] = np.diff(velocity[kpt])/np.diff(time[:-1])
print(displacement)