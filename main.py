from typing import Union

from fastapi import FastAPI
from settings import Settings
import docker
import logging

settings = Settings()
app = FastAPI()
logger = logging.getLogger(__name__)
client_docker = docker.from_env()

def launch_docker_command(cmd):
    cmd = '/usr/local/bin/app/tesla-control -vin %s -ble -key-name /private.pem -key-file /private.pem %s' % (settings.vin, cmd)
    client_docker.containers.run(
        image=settings.docker_image_tesla_vehicle_command, 
        command=cmd,
        mounts=[
            docker.types.Mount(
                source=settings.private_key_file, 
                target='/private.pem', 
                read_only=True,
                type='bind'
            )
        ],
        remove=True,
        network_mode='host',
        privileged=True,
    )


@app.get("/")
def read_root():
    return {"name": settings.app_name, "version": settings.version }

@app.get("/commands")
def list_vehicle_commands():
    return {"commands": settings.commands}

@app.post("/command/{command}")
def send_a_vehicle_command(command: str):
    error=False
    if(command in settings.commands):
        launch_docker_command(command)
        ret='ok'
    else:
        error=True
        ret='Unknown command'
        logger.error(f"Unknown command !")
    return {"error": error, "message": ret }

@app.post("/command/{command}/{value}")
def send_a_vehicle_command_with_a_value(command: str, value: str):
    error=False
    if(command in settings.commands):
        launch_docker_command(command + ' ' + value)
        ret='ok'
    else:
        error=True
        ret='Unknown command'
        logger.error(f"Unknown command !")
    return {"error": error, "message": ret }