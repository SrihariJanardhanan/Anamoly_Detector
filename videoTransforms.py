import cv2
import numpy as np

# To calculate the Optical Flow for Flow Gate
def getOpticalFlow(video):
    """Calculate dense optical flow of input video
    Args:
        video: the input video with shape of [frames,height,width,channel]. dtype=np.array
    Returns:
        flows_x: the optical flow at x-axis, with the shape of [frames,height,width,channel]
        flows_y: the optical flow at y-axis, with the shape of [frames,height,width,channel]
    """
    # initialize the list of optical flows
    gray_video = []
    for i in range(len(video)):
        img = cv2.cvtColor(video[i], cv2.COLOR_RGB2GRAY)
        gray_video.append(np.reshape(img,(224,224,1)))

    flows = []
    for i in range(0,len(video)-1):
        # calculate optical flow between each pair of frames
        flow = cv2.calcOpticalFlowFarneback(gray_video[i], gray_video[i+1], None, 0.5, 3, 15, 3, 5, 1.2, cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
        # subtract the mean in order to eliminate the movement of camera
        flow[..., 0] -= np.mean(flow[..., 0])
        flow[..., 1] -= np.mean(flow[..., 1])
        # normalize each component in optical flow
        flow[..., 0] = cv2.normalize(flow[..., 0],None,0,255,cv2.NORM_MINMAX)
        flow[..., 1] = cv2.normalize(flow[..., 1],None,0,255,cv2.NORM_MINMAX)
        # Add into list
        flows.append(flow)

    flows.append(np.zeros((224,224,2)))

    return np.array(flows, dtype=np.float32)

# To convert video to Numpy array
def Video2Npy(file_path, resize=(224,224)):
    """Load video and tansfer it into .npy format
    Args:
        file_path: the path of video file
        resize: the target resolution of output video
    Returns:
        frames: gray-scale video
        flows: magnitude video of optical flows
    """
    # Load video
    cap = cv2.VideoCapture(file_path)
    # Get number of frames
    len_frames = int(cap.get(7))
    # Extract frames from video
    try:
        frames = []
        for i in range(len_frames-1):
            _, frame = cap.read()
            frame = cv2.resize(frame,resize, interpolation=cv2.INTER_AREA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.reshape(frame, (224,224,3))
            frames.append(frame)
    except:
        print("Error: ", file_path, len_frames,i)
    finally:
        frames = np.array(frames)
        cap.release()

    # Get the optical flow of video
    flows = getOpticalFlow(frames)
    result = np.zeros((len(flows),224,224,5))
    result[...,:3] = frames
    result[...,3:] = flows

    return result


# For Data Preprocessing
def normalize(data):
    mean = np.mean(data)
    std = np.std(data)
    return (data-mean) / std

def random_flip(video, prob):
    s = np.random.rand()
    if s < prob:
        video = np.flip(m=video, axis=2)
    return video

def uniform_sampling(video, target_frames=64):
    # get total frames of input video and calculate sampling interval
    len_frames = int(len(video))
    interval = int(np.ceil(len_frames/target_frames))
    # init empty list for sampled video and
    sampled_video = []
    for i in range(0,len_frames,interval):
        sampled_video.append(video[i])
    # calculate numer of padded frames and fix it
    num_pad = target_frames - len(sampled_video)
    padding = []
    if num_pad>0:
        for i in range(-num_pad,0):
            try:
                padding.append(video[i])
            except:
                padding.append(video[0])
        sampled_video += padding
    # get sampled video
    return np.array(sampled_video, dtype=np.float32)

def color_jitter(video):
    # range of s-component: 0-1
    # range of v component: 0-255
    s_jitter = np.random.uniform(-0.2,0.2)
    v_jitter = np.random.uniform(-30,30)
    for i in range(len(video)):
        hsv = cv2.cvtColor(video[i], cv2.COLOR_RGB2HSV)
        s = hsv[...,1] + s_jitter
        v = hsv[...,2] + v_jitter
        s[s<0] = 0
        s[s>1] = 1
        v[v<0] = 0
        v[v>255] = 255
        hsv[...,1] = s
        hsv[...,2] = v
        video[i] = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return video