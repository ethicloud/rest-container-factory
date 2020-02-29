# rest-container-factory

Created conainers will join the `ethicloud_default` network created by the docker-ethicloud project.

## Environnements

Environnement variables should be set for this code to run:
* SMTP_USER: needed for passit to send emails
* SMTP_PASSWORD: password for the smtp user

## Tests

Requesting a passit instance.
This will create 2 new containers for passit and it's database.
```bash
curl -X PUT http://<host>:5000/container/<name> -d 'service=passit'
```

Deleting a passit instance.
This will delete the passit container and it's database.
```bash
curl -X DELETE http://<host>:5000/container/<name>
```

## Useful

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
