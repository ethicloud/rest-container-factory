import docker
import os

DOCKER_CLIENT = docker.from_env()
DOCKER_NETWORK = 'ethicloud_default'
SMTP_USER = os.environ['SMTP_USER']
SMTP_PASSWORD = os.environ['SMTP_PASSWORD']


def create_postgresql_container(name, password):
    return DOCKER_CLIENT.containers.create(
        image='postgres',
        environment={'POSTGRES_PASSWORD': password},
        name='{}-postgres'.format(name),
        network=DOCKER_NETWORK
    )


def create_passit_container(name, db_name, db_password):
    v = {
        'service': name + '-passit',
        'db_password': db_password,
        'db_name': db_name,
        'smtp_user': SMTP_USER,
        'smtp_password': SMTP_PASSWORD
    }
    return DOCKER_CLIENT.containers.create(
        image="passit/passit:stable",
        command="bin/start.sh",
        environment={
            'DATABASE_URL': 'postgres://postgres:{db_password}@{db_name}:5432/postgres'.format(**v),
            'SECRET_KEY': 'myscecretkeypasswordlol',
            'IS_DEBUG': 'False',
            'EMAIL_URL': 'smtp+ssl://{smtp_user}:{smtp_password}@smtp.gmail.com:465'.format(**v),
            'DEFAULT_FROM_EMAIL': "passit@something.com",
            'EMAIL_CONFIRMATION_HOST': "https://{service}.local".format(**v)
        },
        name='{service}'.format(**v),
        links={db_name: None},
        labels={
            'traefik.enable': 'true',
            'traefik.docker.network': 'default',
            'traefik.http.middlewares.redirect-middleware.redirectscheme.scheme': 'https',
            'traefik.http.services.{service}.loadbalancer.server.port'.format(**v): '8080',
            'traefik.http.routers.{service}-router.entrypoints'.format(**v): 'web',
            'traefik.http.routers.{service}-router.rule'.format(**v): 'Host(`{service}.local`)'.format(**v),
            'traefik.http.routers.{service}-router.middlewares'.format(**v): 'redirect-middleware',
            'traefik.http.routers.{service}secure-router.entrypoints'.format(**v): 'websecure',
            'traefik.http.routers.{service}secure-router.tls'.format(**v): 'true',
            'traefik.http.routers.{service}secure-router.rule'.format(**v): 'Host(`{service}.local`)'.format(**v)
        },
        network=DOCKER_NETWORK
    )


def build_passit(name):
    password = 'P@ssw0rd' # TODO
    database = create_postgresql_container(name, password)
    passit = create_passit_container(name, database.name, password)
    database.start()
    passit.start()
