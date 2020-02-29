import docker
import os

def build_passit(name):
    client = docker.from_env()
    # TODO : refacto string format
    db_name = "passit_db-" + name
    db_password = "s3cr3t"
    passit_name = "passit-" + name
    smtp_user = os.environ['SMTP_USER']
    smtp_password = os.environ['SMTP_PASSWORD']
    network = 'ethicloud_default'

    database = client.containers.create(
        image="postgres",
        environment={'POSTGRES_PASSWORD': db_password},
        name=db_name,
        network=network
    )

    passit = client.containers.create(
        image="passit/passit:stable",
        command="bin/start.sh",
        environment={
            'DATABASE_URL': 'postgres://postgres:{}@{}:5432/postgres'.format(db_password, db_name),
            'SECRET_KEY': 'myscecretkeypasswordlol',
            'IS_DEBUG': 'False',
            'EMAIL_URL': 'smtp+ssl://{}:{}@smtp.gmail.com:465'.format(smtp_user, smtp_password),
            'DEFAULT_FROM_EMAIL': "passit@something.com",
            'EMAIL_CONFIRMATION_HOST': "https://{}.local".format(passit_name)
        },
        name=passit_name,
        links={db_name:None},
        labels={
          'traefik.enable': 'true',
          'traefik.docker.network': 'default',
          'traefik.http.services.{}-service.loadbalancer.server.port'.format(passit_name): '8080',
          'traefik.http.middlewares.redirect-middleware.redirectscheme.scheme': 'https',
          'traefik.http.routers.{}-router.entrypoints'.format(passit_name): 'web',
          'traefik.http.routers.{}-router.rule'.format(passit_name): 'Host(`{}.local`)'.format(passit_name),
          'traefik.http.routers.{}-router.middlewares'.format(passit_name): 'redirect-middleware',
          'traefik.http.routers.{}secure-router.entrypoints'.format(passit_name): 'websecure',
          'traefik.http.routers.{}secure-router.tls'.format(passit_name): 'true',
          'traefik.http.routers.{}secure-router.rule'.format(passit_name): 'Host(`{}.local`)'.format(passit_name)
        },
        network=network
    )

    database.start()
    passit.start()
