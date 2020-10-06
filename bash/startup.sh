#!/bin/sh

# cd to the rest of the startup scripts
cd startup/

# start CMS
sh cms.sh &

# start python backend
sh py_backend.sh &

# start pose estimator
pose.bat &

# start Unreal Engine program
sh ue.sh &

wait

echo ALL STARTUP DONE