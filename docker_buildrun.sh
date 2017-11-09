#!/bin/bash
docker build -t rgbhsv .
docker run -it --rm --name rgbhsv -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix rgbhsv
