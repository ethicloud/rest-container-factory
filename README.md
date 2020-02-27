# rest-container-factory

To run the container:
```bash
docker build -t rcf
docker run \
  -e SMTP_USER='<gmail user>' \
  -e SMTP_PASSWORD='<gmail password>' \
  --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock \
  --mount type=bind,source=/var/lib/docker,destination=/var/lib/docker \
  -p 5000:8000 rcf
```

You can then ask the server to create containers with the following requests:
```bash
curl
  --url http://yseult:5000/container/first \
  --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
  --form service=passit \
  --form =```

curl --request PUT \
  --url http://yseult:5000/container/two \
  --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
  --form service=passit \
  --form =
```

Containers will join the `passit_default` network created by the traefik docker-compose in passit project.
Traefik needs to be launched first.
