# Image stream

Testing how to send video images from a webcam to the server using sockets and then predicting using Detectron2.

```
/---\       --------   socket   --------   predict  /-----\
|CAM| >---< |Client| ---------> |Server| >--------< |Model|
\---/       --------   r_img    --------            \-----/
                                    |
                              socket|(o_img, p_img)
                                    v
                                ---------
                                |Monitor|
                                ---------
                                    /\ show
                                   /  \
                                  /    \
                              /-----\ /-----\
                              |o_img| |p_img|
                              \-----/ \-----/
r_img --> raw image
o_img --> original image
p_img --> predicted image
```

## Startup sequence

Monitor -> Server -> Client

## Monitor
Receive data from server.
```
pyhton3 monitor.py
```
## Server
Receive data from client, make prediction and send the result to the monitor.

First build or run the container.
```
docker-compose run --service-ports --volume=/home/davamix/Development/python/image-stream:/tmp:rw detectron2
```

If the `Dockerfile` has changed or any file should be copied again to the container, build with:
```
USER_ID=$UID docker-compose build detectron2
```

## Client
Send the images captured by the webcam to the server.

```
python3 client.py
```
