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


fig, axes = plt.subplots(9, 2,figsize=(15,30))
flat_axes = [item for sublist in axes for item in sublist]

for i, ax in enumerate(flat_axes):
    ax.grid()
    ax.set_ylim(-.6,.6)
    ax.set_xlabel('Frame (time ~.4 sec)')
    ax.set_ylabel('X measure')
    # add 1 to skip second plot
    if i == 0:
         ax.set_title(keypoints[i] + ' x/y displacement')
    elif i == 1:
        continue
    else:
        ax.set_title(keypoints[i-1] + ' x/y displacement')

fig.tight_layout()

x_smooth = np.linspace(min(time), max(time), 300)
displacement = {}

for i, kpt in enumerate(keypoints):
    xsquared = np.square(np.asarray(kpt_dict_x[kpt]))
    ysquared = np.square(np.asarray(kpt_dict_y[kpt]))
    displacement[kpt] = np.sqrt(xsquared + ysquared)
    y_smooth = spline(time, displacement[kpt], x_smooth)
    if i < 1:
        flat_axes[i].plot(x_smooth, y_smooth,'r-')
    elif i >= 1:
        flat_axes[i+1].plot(x_smooth, y_smooth,'r-')
        
fig.savefig('displacement.png')
for x in time:
    lines = []
    for i, kpt in enumerate(keypoints):
        if i < 1:        
            lines.append(flat_axes[i].axvline(x,color='m'))
        elif i >= 1:
            lines.append(flat_axes[i+1].axvline(x,color='m'))

    fig.savefig('./displacement/displacement_' + format(x, '04d') + '.png')
    for x in lines:
        x.remove()

# fig, axes = plt.subplots(9, 2,figsize=(15,30))
# flat_axes = [item for sublist in axes for item in sublist]

# for i, ax in enumerate(flat_axes):
#     ax.grid()
#     ax.set_ylim(-.6,.6)
#     ax.set_xlabel('Frame (time ~.4 sec)')
#     ax.set_ylabel('X measure')
#     # add 1 to skip second plot
#     if i == 0:
#          ax.set_title(keypoints[i] + ' X derivative')
#     elif i == 1:
#         continue
#     else:
#         ax.set_title(keypoints[i-1] + ' X derivative')

# fig.tight_layout()

# # # velocity
# x_smooth = np.linspace(min(time), max(time)-1, 300)
# for i, kpt in enumerate(keypoints):
#     dXdV = np.diff(displacement[kpt])/np.diff(time)
#     y_smooth = spline(time[:-1], dXdV , x_smooth)
#     if i < 1:
#         flat_axes[i].plot(x_smooth, y_smooth,'b-')
#     elif i >= 1:
#         flat_axes[i+1].plot(x_smooth, y_smooth,'b-')
# #fig.savefig('velocity.png')

# for x in time:
#     lines = []
#     for i, kpt in enumerate(keypoints):
#         if i < 1:        
#             lines.append(flat_axes[i].axvline(x,color='m'))
#         elif i >= 1:
#             lines.append(flat_axes[i+1].axvline(x,color='m'))

#     fig.savefig('./velocity/velocity' + format(x, '04d') + '.png')
#     for x in lines:
#         x.remove()

# acceleration
# x_smooth = np.linspace(min(time), max(time)-2, 300)
# for i, kpt in enumerate(keypoints):
#     dXdV = np.diff(displacement[kpt])/np.diff(time)
#     ddXdV = np.diff(dXdV)/np.diff(time[:-1])
#     y_smooth = spline(time[:-2], ddXdV , x_smooth)
#     if i < 1:
#         flat_axes[i].plot(x_smooth, y_smooth,'g-')
#     elif i >= 1:
#         flat_axes[i+1].plot(x_smooth, y_smooth,'g-')
# fig.savefig('acceleration.png')

# for x in time:
#     lines = []
#     for i, kpt in enumerate(keypoints):
#         if i < 1:        
#             lines.append(flat_axes[i].axvline(x,color='m'))
#         elif i >= 1:
#             lines.append(flat_axes[i+1].axvline(x,color='m'))

#     fig.savefig('./acceleration/acceleration' + format(x, '04d') + '.png')
#     for x in lines:
#         x.remove()