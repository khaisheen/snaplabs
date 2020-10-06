echo starting up pose estimator...

cd "../../pose_est"

set root=C:\Users\pault\Anaconda3
call %root%\Scripts\activate.bat %root%
call conda activate pytorch_env
python demo13.py --model human-pose-estimation-3d.pth --video 0

echo DONE! Pose estimator up and running.

