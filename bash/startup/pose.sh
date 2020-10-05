#!/bin/sh

echo starting up pose estimator...

cd "../../pose_est"

python3 demo13.py --model human-pose-estimation-3d.pth --video 0

echo DONE! Pose estimator up and running.

