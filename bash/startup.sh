#!/bin/bash

# start CMS
sh cms.sh &

# start python backend
sh py_backend.sh &

# start pose estimator
sh pose.sh &

# start Unreal Engine program
sh ue.sh &

wait

echo ALL STARTUP DONE