# OpenCVBase

Basic openCV2 staff.

## CPP

QT application showing image processing features of OpenCV

```
cmake --build <project-dir>/cmake-build-debug --target BaseCv -- -j 6
```

## Python

1. IO Camera(io_camera.py) - Get video from camera
2. IO Camera(io_camera_2.py) - Get video from camera on mouse click.
3. IO Image(io_image.py) - Read and write image with some modifications.
4. Face Detection(face_detect_camera/detect.py) - Detect and track face on video from camera.
5. Cameo (cameo/cameo.py)- Detect face and put background. 


### Run
```
cd Python

pip install cv2

python <script-name>.py
```


## Notes

- Run video scripts as a root(unix) or admin(win)

- For cameo and tracking  add from openCV dir to project:

```
haarcascade_eye.xml
haarcascade_frontalface_alt.xml
haarcascade_mcs_mouth.xml
haarcascade_mcs_nose.xml
```

- Python script names are in ().

