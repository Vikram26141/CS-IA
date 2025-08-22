import cv2, numpy as np
from sklearn.cluster import KMeans

def team_from_bbox(bbox_img):
    hsv = cv2.cvtColor(bbox_img, cv2.COLOR_BGR2HSV)
    pixels = hsv.reshape(-1, 3)
    k = KMeans(n_clusters=2, random_state=0).fit(pixels)

    centers = k.cluster_centers_
    team = np.argmax(centers[:, 2])
    return int(team)
