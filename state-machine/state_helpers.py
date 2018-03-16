def generate_states(count):
    states = []
    for x in range(count):
        string = 'State-' + str(x)
        states.append(string)
    return states

def generate_linear_triggers(states):
    pass

def invert_keypoints(keypoints):
    kpts_inverted = []
    for frame in keypoints:
        tmp = []
        for i, point in enumerate(frame):
            tmp.append([point[1], point[0] * -1])
        kpts_inverted.append(tmp)
    return kpts_inverted