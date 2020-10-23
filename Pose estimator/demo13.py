from argparse import ArgumentParser
import json
import os

import cv2
import numpy as np

from modules.input_reader import VideoReader, ImageReader
from modules.custom_draw import draw_poses_2, draw_poses_3
from modules.custom_parse_pose import parse_poses_2d

import time

import win32api
#import mouse
#from pymouse import PyMouse
#m = PyMouse()

target_width = 1920
target_height = 1080


def clipped(_x, _y):
    x = max(0, min(target_width, _x))
    y = max(0, min(target_height, _y))
    return (x,y)

def calcHandPos(x, y, w, h):
    pass
    # b_width = frame.shape[1]
    # b_height = frame.shape[0]
    # x_offset = int(b_width * x_scale / 2 - b_width / 2)
    # y_offset = int(b_height * y_scale / 2 - b_height / 2)
    # hand_pos = (b_width - wrist_pos[0], wrist_pos[1])
    # cursorX = int((hand_pos[0] * x_scale - x_offset)/b_width * target_width)
    # cursorY = int((hand_pos[1] * y_scale - y_offset)/b_height * target_height) + y_adjust_2
    # hand_pos = clipped(cursorX, cursorY)
    # cur_pos = hand_pos if cur_pos == None else (hand_pos[0] * ema_w + cur_pos[0] * (1-ema_w), hand_pos[1] * ema_w + cur_pos[1] * (1-ema_w))

def runNormal(fx, delay ,esc_code):
    x_adjust = 3
    y_adjust = 3
    y_adjust_2 = 200
    mean_time = 0
    input_scale_mult = 1

    ema_w = 0.3
    cur_pos = None
    hand_pos = None
    for frame in frame_provider:
        current_time = cv2.getTickCount()
        if frame is None:
            break
        input_scale = base_height / frame.shape[0] * input_scale_mult
        scaled_img = cv2.resize(frame, dsize=None, fx=input_scale, fy=input_scale)
        scaled_img = scaled_img[:, 0:scaled_img.shape[1] - (scaled_img.shape[1] % stride)]  # better to pad, but cut out for demo
        if fx < 0:  # Focal length is unknown
            fx = np.float32(0.8 * frame.shape[1])

        inference_result = net.infer(scaled_img)

        poses_2d = parse_poses_2d(inference_result, input_scale, stride, fx, is_video)
        edges = []

        wrist_pos, person_height = draw_poses_3(frame, poses_2d)
        # Framerate Calculation
        # current_time = (cv2.getTickCount() - current_time) / cv2.getTickFrequency()
        # if mean_time == 0:
        #     mean_time = current_time
        # else:
        #     mean_time = mean_time * 0.95 + current_time * 0.05
        #print('FPS: {}'.format(int(1 / mean_time * 10) / 10))
        if wrist_pos is not None:
            x_scale = x_adjust
            y_scale = y_adjust
            b_width = frame.shape[1]
            b_height = frame.shape[0]
            x_offset = int(b_width * x_scale / 2 - b_width / 2)
            y_offset = int(b_height * y_scale / 2 - b_height / 2)
            hand_pos = (b_width - wrist_pos[0], wrist_pos[1])
            cursorX = int((hand_pos[0] * x_scale - x_offset)/b_width * target_width)
            cursorY = int((hand_pos[1] * y_scale - y_offset)/b_height * target_height) + y_adjust_2
            hand_pos = clipped(cursorX, cursorY)
            cur_pos = hand_pos if cur_pos == None else (int(hand_pos[0] * ema_w + cur_pos[0] * (1-ema_w)), int(hand_pos[1] * ema_w + cur_pos[1] * (1-ema_w)))
            
            win32api.SetCursorPos(cur_pos)
            #m.move(hand_pos[0], hand_pos[1])

            #mouse.move(hand_pos[0], hand_pos[1], absolute=True, duration=0.1)
            #print(hand_pos)
        
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, f'POS: {hand_pos}', (40, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
        cv2.imshow('Visualiser', frame)

        key = cv2.waitKey(delay)
        if key == esc_code:
            break


fx = None
delay = 1
esc_code = 27

if __name__ == '__main__':
    parser = ArgumentParser(description='Lightweight 3D human pose estimation demo. '
                                        'Press esc to exit, "p" to (un)pause video or process next image.')
    parser.add_argument('-m', '--model',
                        help='Required. Path to checkpoint with a trained model '
                             '(or an .xml file in case of OpenVINO inference).',
                        type=str, required=True)
    parser.add_argument('--video', help='Optional. Path to video file or camera id.', type=str, default='')
    parser.add_argument('-d', '--device',
                        help='Optional. Specify the target device to infer on: CPU or GPU. '
                             'The demo will look for a suitable plugin for device specified '
                             '(by default, it is GPU).',
                        type=str, default='GPU')
    parser.add_argument('--use-openvino',
                        help='Optional. Run network with OpenVINO as inference engine. '
                             'CPU, GPU, FPGA, HDDL or MYRIAD devices are supported.',
                        action='store_true')
    parser.add_argument('--images', help='Optional. Path to input image(s).', nargs='+', default='')
    parser.add_argument('--height-size', help='Optional. Network input layer height size.', type=int, default=256)
    parser.add_argument('--extrinsics-path',
                        help='Optional. Path to file with camera extrinsics.',
                        type=str, default=None)
    parser.add_argument('--fx', type=np.float32, default=-1, help='Optional. Camera focal length.')
    args = parser.parse_args()

    if args.video == '' and args.images == '':
        raise ValueError('Either --video or --image has to be provided')

    stride = 8
    if args.use_openvino:
        from modules.inference_engine_openvino import InferenceEngineOpenVINO
        net = InferenceEngineOpenVINO(args.model, args.device)
    else:
        from modules.inference_engine_pytorch import InferenceEnginePyTorch
        net = InferenceEnginePyTorch(args.model, args.device)

    file_path = args.extrinsics_path
    if file_path is None:
        file_path = os.path.join('data', 'extrinsics.json')
    with open(file_path, 'r') as f:
        extrinsics = json.load(f)
    R = np.array(extrinsics['R'], dtype=np.float32)
    t = np.array(extrinsics['t'], dtype=np.float32)

    frame_provider = ImageReader(args.images)
    is_video = False
    if args.video != '':
        frame_provider = VideoReader(args.video)
        is_video = True
    base_height = args.height_size

    fx = args.fx
    delay = 1
    esc_code = 27
    mean_time = 0
    
    runNormal(fx, delay, esc_code)
    