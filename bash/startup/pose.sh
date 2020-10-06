#!/bin/sh

echo starting up pose estimator...

cd "../../pose_est"

conda init
conda activate pose_env
python demo13.py --model human-pose-estimation-3d.pth --video 0

echo DONE! Pose estimator up and running.

