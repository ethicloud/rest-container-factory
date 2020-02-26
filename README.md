# rest-container-factory

To run the container:
```
docker run \
  --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock \
  --mount type=bind,source=/var/lib/docker,destination=/var/lib/docker \
  -p 5000:8000 rcf
```
