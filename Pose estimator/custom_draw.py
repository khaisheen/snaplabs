import math

import cv2
import numpy as np


theta, phi = 3.1415/4, -3.1415/6
should_rotate = False
scale_dx = 800
scale_dy = 800

screen_width = 1920
screen_height = 1080

body_edges = np.array(
    [[0, 1],  # neck - nose
     [1, 16], [16, 18],  # nose - l_eye - l_ear
     [1, 15], [15, 17],  # nose - r_eye - r_ear
     [0, 3], [3, 4], [4, 5],     # neck - l_shoulder - l_elbow - l_wrist
     [0, 9], [9, 10], [10, 11],  # neck - r_shoulder - r_elbow - r_wrist
     [0, 6], [6, 7], [7, 8],        # neck - l_hip - l_knee - l_ankle
     [0, 12], [12, 13], [13, 14]])  # neck - r_hip - r_knee - r_ankle



def draw_poses(img, poses_2d):
    center_x = img.shape[1] / 2
    wrist_pos = None
    eye_pos = None
    nose_pose = None
    my_pose = None
    my_found = None

    for pose_id in range(len(poses_2d)):
        pose = np.array(poses_2d[pose_id][0:-1]).reshape((-1, 3)).transpose()
        was_found = pose[2, :] > 0

        human_detected = was_found[15] and was_found[16]
        if not is_human_present(pose, was_found, center_x):
            continue
        
        # Eyes that are lowest
        current_eye_pos = (pose[1,16] + pose[1,15])/2
        if eye_pos is None or current_eye_pos > eye_pos:
            eye_pos = current_eye_pos
            my_pose = pose
            my_found = was_found
        else:
            continue
            
    if my_found is None:
        return None
    
    for edge in body_edges:
        if my_found[edge[0]] and my_found[edge[1]]:
            cv2.line(img, tuple(my_pose[0:2, edge[0]].astype(int)), tuple(my_pose[0:2, edge[1]].astype(int)),
                        (255, 255, 0), 4, cv2.LINE_AA)

    for kpt_id in range(my_pose.shape[1]):
        if my_pose[2, kpt_id] != -1:
            temp_color = (0, 255, 255)
            temp_size = 3
            if kpt_id == 11:
                wrist_pos = my_pose[0:2, kpt_id]
                temp_color = (0, 0, 255)
                #temp_size = 20
            
            cv2.circle(img, tuple(my_pose[0:2, kpt_id].astype(int)), temp_size, temp_color, -1, cv2.LINE_AA)
        
    return wrist_pos


def draw_poses_2(img, poses_2d):
    center_x = img.shape[1] / 2
    wrist_pos = None
    eye_pos = None
    nose_pose = None
    my_pose = None
    my_found = None

    for pose_id in range(len(poses_2d)):
        pose = np.array(poses_2d[pose_id][0:-1]).reshape((-1, 3)).transpose()
        was_found = pose[2, :] > 0

        human_detected = was_found[15] and was_found[16]
        if not is_human_present(pose, was_found, center_x):
            continue
        
        # Eyes that are lowest
        current_eye_pos = (pose[1,16] + pose[1,15])/2
        if eye_pos is None or current_eye_pos > eye_pos:
            eye_pos = current_eye_pos
            my_pose = pose
            my_found = was_found
        else:
            continue
        
        # Distance between Eyes method
        # current_eye_pos = abs(pose[1,16] - pose[1,15])/2
        # if eye_pos is None or current_eye_pos > eye_pos:
        #    eye_pos = current_eye_pos
        #    my_pose = pose
        #    my_found = was_found
        # else:
        #    continue

        # Distance of eyes from center line
        #current_eye_pos = (pose[0,16] + pose[0,15])/2
        #if eye_pos is None or abs(current_eye_pos-center_x) < abs(eye_pos-center_x):
        #    eye_pos = current_eye_pos
        #    my_pose = pose
        #    my_found = was_found
        #else:
        #    continue
            
    if my_found is None:
        return None
    
    for edge in body_edges:
        if my_found[edge[0]] and my_found[edge[1]]:
            cv2.line(img, tuple(my_pose[0:2, edge[0]].astype(int)), tuple(my_pose[0:2, edge[1]].astype(int)),
                        (255, 255, 0), 4, cv2.LINE_AA)

    for kpt_id in range(my_pose.shape[1]):
        if my_pose[2, kpt_id] != -1:
            cv2.circle(img, tuple(my_pose[0:2, kpt_id].astype(int)), 3, (0,255,255), -1, cv2.LINE_AA)
    
    # Left wrist
    left_wrist = my_pose[0:2, 5]
    has_left = my_pose[2, 5] != -1
    # Right wrist
    right_wrist = my_pose[0:2, 11]
    has_right = my_pose[2, 11] != -1
    if has_left and has_right: 
        wrist_pos = left_wrist if left_wrist[1] < right_wrist[1] else right_wrist
        cv2.circle(img, tuple(wrist_pos.astype(int)), 8, (0,0,255), -1, cv2.LINE_AA)
    elif has_left: 
        wrist_pos = left_wrist
        cv2.circle(img, tuple(wrist_pos.astype(int)), 8, (0,0,255), -1, cv2.LINE_AA)
    elif has_right: 
        wrist_pos = right_wrist
        cv2.circle(img, tuple(wrist_pos.astype(int)), 8, (0,0,255), -1, cv2.LINE_AA)
        
    return wrist_pos


def draw_poses_3(img, poses_2d):
    center_x = img.shape[1] / 2
    wrist_pos = None
    eye_pos = None
    ankle_pos = None
    nose_pose = None
    my_pose = None
    my_found = None

    for pose_id in range(len(poses_2d)):
        pose = np.array(poses_2d[pose_id][0:-1]).reshape((-1, 3)).transpose()
        was_found = pose[2, :] > 0

        human_detected = was_found[15] and was_found[16]
        if not is_human_present(pose, was_found, center_x):
            continue
        
        # Lowest ankles
        current_ankle_pos = (pose[1,8] + pose[1,14])/2
        if ankle_pos is None or current_ankle_pos > ankle_pos:
            ankle_pos = current_ankle_pos
            my_pose = pose
            my_found = was_found
        else:
            continue

            
    if my_found is None:
        return None, None
    
    for edge in body_edges:
        if my_found[edge[0]] and my_found[edge[1]]:
            cv2.line(img, tuple(my_pose[0:2, edge[0]].astype(int)), tuple(my_pose[0:2, edge[1]].astype(int)),
                        (255, 255, 0), 4, cv2.LINE_AA)

    for kpt_id in range(my_pose.shape[1]):
        if my_pose[2, kpt_id] != -1:
            cv2.circle(img, tuple(my_pose[0:2, kpt_id].astype(int)), 3, (0,255,255), -1, cv2.LINE_AA)
    
    # Left wrist
    left_wrist = my_pose[0:2, 5]
    has_left = my_pose[2, 5] != -1
    # Right wrist
    right_wrist = my_pose[0:2, 11]
    has_right = my_pose[2, 11] != -1
    if has_left and has_right: 
        wrist_pos = left_wrist if left_wrist[1] < right_wrist[1] else right_wrist
        cv2.circle(img, tuple(wrist_pos.astype(int)), 8, (0,0,255), -1, cv2.LINE_AA)
    elif has_left: 
        wrist_pos = left_wrist
        cv2.circle(img, tuple(wrist_pos.astype(int)), 8, (0,0,255), -1, cv2.LINE_AA)
    elif has_right: 
        wrist_pos = right_wrist
        cv2.circle(img, tuple(wrist_pos.astype(int)), 8, (0,0,255), -1, cv2.LINE_AA)
        
    person_height = abs(ankle_pos-my_pose[1,1]) / 580 * 170
    return wrist_pos, person_height


def is_human_present(pose, found_arr, center_x):
    eye_dist_threshold = 20
    center_dist = 300
    return found_arr[15] and found_arr[16] and \
            pose[0,16] - pose[0,15] > eye_dist_threshold and \
            abs(pose[0,1] - center_x) < center_dist and \
            found_arr[8] and found_arr[14]
        


