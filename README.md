# Image stream

Testing how to send video images from a webcam to the server using sockets and then predicting using Detectron2.

```
/---\       --------   socket   --------   predict  /-----\
|CAM| >---< |Client| ---------> |Server| >--------< |Model|
\---/       --------            --------            \-----/
```

## Server
```
docker-compose run --service-ports --volume=/home/davamix/Development/python/image-stream:/tmp:rw detectron2
```

## Client
```
python3 client.py
```