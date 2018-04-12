from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pickle
import copy

with open('test.pickle', 'rb') as handle:
    kpts = pickle.load(handle, encoding='bytes')

keypoints = [
        'nose',
        'left_eye',
        'right_eye',
        'left_ear',
        'right_ear',
        'left_shoulder',
        'right_shoulder',
        'left_elbow',
        'right_elbow',
        'left_wrist',
        'right_wrist',
        'left_hip',
        'right_hip',
        'left_knee',
        'right_knee',
        'left_ankle',
        'right_ankle'
    ]


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

for frame in kpts:
    for i, point in enumerate(frame):
        kpt_dict_x[keypoints[i]].append(point[1])
        kpt_dict_y[keypoints[i]].append(point[0])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

part='left_hip'
x = kpt_dict_x[part]
y = kpt_dict_y[part]
time = list(range(len(x)))

ax.plot(x, y, time, c='r', marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('time')

plt.show()
