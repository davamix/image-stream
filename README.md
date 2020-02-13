# Image stream

Testing how to send video images from a webcam to the server using sockets and then predicting using Detectron2.

```
/---\       --------   socket   --------   predict  /-----\
|CAM| >---< |Client| ---------> |Server| >--------< |Model|
\---/       --------            --------            \-----/
                                    |
                                    |socket
                                    v
                                ---------
                                |Monitor|
                                ---------
```

## Server
First build or run the container.
```
docker-compose run --service-ports --volume=/home/davamix/Development/python/image-stream:/tmp:rw detectron2
```

If the `Dockerfile` is changed, build with:
```
USER_ID=$UID docker-compose build detectron2
```

## Client
```
python3 client.py
```