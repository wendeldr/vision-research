import numpy as np
import matplotlib.pyplot as plt
import pickle

def get_keypoints():
    """Get the COCO keypoints and their left/right flip coorespondence map."""
    # Keypoints are not available in the COCO json for the test split, so we
    # provide them here.
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
    keypoint_flip_map = {
        'left_eye': 'right_eye',
        'left_ear': 'right_ear',
        'left_shoulder': 'right_shoulder',
        'left_elbow': 'right_elbow',
        'left_wrist': 'right_wrist',
        'left_hip': 'right_hip',
        'left_knee': 'right_knee',
        'left_ankle': 'right_ankle'
    }
    return keypoints, keypoint_flip_map

def kp_connections(keypoints):
    kp_lines = [
        [keypoints.index('left_eye'), keypoints.index('right_eye')],
        [keypoints.index('left_eye'), keypoints.index('nose')],
        [keypoints.index('right_eye'), keypoints.index('nose')],
        [keypoints.index('right_eye'), keypoints.index('right_ear')],
        [keypoints.index('left_eye'), keypoints.index('left_ear')],
        [keypoints.index('right_shoulder'), keypoints.index('right_elbow')],
        [keypoints.index('right_elbow'), keypoints.index('right_wrist')],
        [keypoints.index('left_shoulder'), keypoints.index('left_elbow')],
        [keypoints.index('left_elbow'), keypoints.index('left_wrist')],
        [keypoints.index('right_hip'), keypoints.index('right_knee')],
        [keypoints.index('right_knee'), keypoints.index('right_ankle')],
        [keypoints.index('left_hip'), keypoints.index('left_knee')],
        [keypoints.index('left_knee'), keypoints.index('left_ankle')],
        [keypoints.index('right_shoulder'), keypoints.index('left_shoulder')],
        [keypoints.index('right_hip'), keypoints.index('left_hip')],
    ]
    return kp_lines

def convert_from_cls_format(cls_boxes, cls_keyps):
    """Convert from the class boxes/segms/keyps format generated by the testing
    code.
    """
    box_list = [b for b in cls_boxes if len(b) > 0]
    if len(box_list) > 0:
        boxes = np.concatenate(box_list)
    else:
        boxes = None
    if cls_keyps is not None:
        keyps = [k for klist in cls_keyps for k in klist]
    else:
        keyps = None
    classes = []
    for j in range(len(cls_boxes)):
        classes += [j] * len(cls_boxes[j])
    return boxes, keyps, classes


def viz_keypoints_3D(im_name, boxes, keypoints=None, thresh=0.6,
        kp_thresh=2, dpi=200, box_alpha=1, dataset=None):

    if isinstance(boxes, list):
        boxes, keypoints, classes = convert_from_cls_format(
            boxes, keypoints)

    if boxes is None or boxes.shape[0] == 0 or max(boxes[:, 4]) < thresh:
        return

    dataset_keypoints, _ = get_keypoints()

    kp_lines = kp_connections(dataset_keypoints)

    cmap = plt.get_cmap('rainbow')
    colors = [cmap(i) for i in np.linspace(0, 1, len(kp_lines) + 2)]
    #

    # ax.spines['left'].set_position('zero')
    # ax.spines['bottom'].set_position('zero')

    # #ax.axis('off')
    # fig.add_axes(ax)


    # # Display in largest to smallest order to reduce occlusion
    areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    sorted_inds = np.argsort(-areas)
    #
    # mask_color_id = 0

    bbox = boxes[sorted_inds[0], :4]
    score = boxes[sorted_inds[0], -1]

    if score < thresh:
        return

    #https://stackoverflow.com/questions/1373035/how-do-i-scale-one-rectangle-to-the-maximum-size-possible-within-another-rectang
    scaler = min(0.7 / (bbox[2] - bbox[0]), 0.7 / (bbox[3] - bbox[1]))

    bbox = [x * scaler for x in bbox]
    bbox_x_center = bbox[0] + (bbox[2] - bbox[0])/2
    bbox_y_center = bbox[1] + (bbox[3] - bbox[1])/2

    bbox = [bbox[0]-bbox_x_center,
            bbox[1]-bbox_y_center,
            bbox[2]-bbox_x_center,
            bbox[3]-bbox_y_center]
    print(bbox)

    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])

    # show box (off by default)
    ax.add_patch(
        plt.Rectangle((bbox[0], bbox[1]),
                      (bbox[2] - bbox[0]),
                      (bbox[3] - bbox[1]),
                      fill=False, edgecolor='g',
                      linewidth=0.5)
    )

    # show keypoints
    if keypoints is not None:
        kps = keypoints[sorted_inds[0]]
        plt.autoscale(False)

        # plot lines
        for l in range(len(kp_lines)):
            i1 = kp_lines[l][0]
            i2 = kp_lines[l][1]
            # plot lines btw all keypoints except backbone/neck
            if kps[2, i1] > kp_thresh and kps[2, i2] > kp_thresh:
                x = [kps[0, i1] * scaler - bbox_x_center, kps[0, i2] * scaler - bbox_x_center]
                y = [kps[1, i1] * scaler - bbox_y_center, kps[1, i2] * scaler - bbox_y_center]
                y = [y[0]*-1, y[1]*-1]
                line = plt.plot(x, y)
                plt.setp(line, color=colors[l], linewidth=1.0, alpha=0.7)
            
            # plot points
            if kps[2, i1] > kp_thresh:
                plt.plot(
                    kps[0, i1] * scaler - bbox_x_center, (kps[1, i1] * scaler - bbox_y_center) * -1, '.', color=colors[l],
                    markersize=3.0, alpha=0.7)

            if kps[2, i2] > kp_thresh:
                plt.plot(
                    kps[0, i2] * scaler - bbox_x_center, (kps[1, i2] * scaler - bbox_y_center) * -1, '.', color=colors[l],
                    markersize=3.0, alpha=0.7)
        # print(i1)
        # print(i2)
        # print(kps)
        # print(kps[2, :])
        # print(kps[2, i1])
        # print(kps[2, i2])
        # add mid shoulder / mid hip for better visualization
        mid_shoulder = (
            kps[:2, dataset_keypoints.index('right_shoulder')] +
            kps[:2, dataset_keypoints.index('left_shoulder')]) / 2.0
        sc_mid_shoulder = np.minimum(
            kps[2, dataset_keypoints.index('right_shoulder')],
            kps[2, dataset_keypoints.index('left_shoulder')])
        mid_hip = (
            kps[:2, dataset_keypoints.index('right_hip')] +
            kps[:2, dataset_keypoints.index('left_hip')]) / 2.0
        sc_mid_hip = np.minimum(
            kps[2, dataset_keypoints.index('right_hip')],
            kps[2, dataset_keypoints.index('left_hip')])
        if (sc_mid_shoulder > kp_thresh and
                kps[2, dataset_keypoints.index('nose')] > kp_thresh):
            x = [mid_shoulder[0] * scaler - bbox_x_center,
                 kps[0, dataset_keypoints.index('nose')] * scaler - bbox_x_center]
            y = [mid_shoulder[1] * scaler - bbox_y_center,
                 kps[1, dataset_keypoints.index('nose')] * scaler - bbox_y_center]
            y = [y[0] * -1, y[1] * -1]
            line = plt.plot(x, y)
            plt.setp(
                line, color=colors[len(kp_lines)], linewidth=1.0, alpha=0.7)
        if sc_mid_shoulder > kp_thresh and sc_mid_hip > kp_thresh:
            x = [mid_shoulder[0] * scaler - bbox_x_center, mid_hip[0] * scaler - bbox_x_center]
            y = [mid_shoulder[1] * scaler - bbox_y_center, mid_hip[1] * scaler - bbox_y_center]
            y = [y[0] * -1, y[1] * -1]
            line = plt.plot(x, y)
            plt.setp(
                line, color=colors[len(kp_lines) + 1], linewidth=1.0,
                alpha=0.7)
    fig.savefig('./figs/keypoint_' + format(asdf, '04d') + '.png')

    plt.pause(0.1)
    # plt.show()
    plt.clf()
    #plt.show()

asdf = 0
fig = plt.figure(figsize=(10, 6))

with open('keypoints.pickle', 'rb') as handle:
    output = pickle.load(handle, encoding='bytes')
    output = sorted(output)

print(output)
# for i, x in enumerate(output):
#     viz_keypoints_3D(i, x[1],x[2])
#     asdf+=1

