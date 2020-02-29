import docker
import os

DOCKER_CLIENT = docker.from_env()
DOCKER_NETWORK = 'ethicloud_default'
SMTP_USER = os.environ['SMTP_USER']
SMTP_PASSWORD = os.environ['SMTP_PASSWORD']


def create_postgresql_container(name, password):
    return DOCKER_CLIENT.containers.create(
        image="postgres",
        environment={'POSTGRES_PASSWORD': password},
        name="{name}-postgres",
        network=DOCKER_NETWORK
    )


def create_passit_container(name, db_name, db_password):
    service = "{name}-passit"
    return DOCKER_CLIENT.containers.create(
        image="passit/passit:stable",
        command="bin/start.sh",
        environment={
            'DATABASE_URL': 'postgres://postgres:{db_password}@{db_name}:5432/postgres',
            'SECRET_KEY': 'myscecretkeypasswordlol',
            'IS_DEBUG': 'False',
            'EMAIL_URL': 'smtp+ssl://{SMTP_USER}:{SMTP_PASSWORD}@smtp.gmail.com:465',
            'DEFAULT_FROM_EMAIL': "passit@something.com",
            'EMAIL_CONFIRMATION_HOST': "https://{service}.local"
        },
        name="{name}-passit",
        links={db_name: None},
        labels={
            'traefik.enable': 'true',
            'traefik.docker.network': 'default',
            'traefik.http.services.{service}-service.loadbalancer.server.port': '8080',
            'traefik.http.middlewares.redirect-middleware.redirectscheme.scheme': 'https',
            'traefik.http.routers.{service}-router.entrypoints': 'web',
            'traefik.http.routers.{service}-router.rule': 'Host(`{service}.local`)',
            'traefik.http.routers.{service}-router.middlewares': 'redirect-middleware',
            'traefik.http.routers.{service}secure-router.entrypoints': 'websecure',
            'traefik.http.routers.{service}secure-router.tls': 'true',
            'traefik.http.routers.{service}secure-router.rule': 'Host(`{service}.local`)'
        },
        network=DOCKER_NETWORK
    )


def build_passit(name):
    password = 'P@ssw0rd' # TODO
    database = create_postgresql_container(name, password)
    passit = create_passit_container(name, database.name, password)
    database.start()
    passit.start()
