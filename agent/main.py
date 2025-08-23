import os
import sys
from typing import Union

from fastapi import FastAPI
from vm import Virtual_Machine

app = FastAPI()

vm = Virtual_Machine()


@app.get("/")
def read_root():
    return {
        "Host": vm.name,
        "CPU": vm.get_cpu(),
        "RAM": vm.get_ram(),
        "Disk": vm.get_disk_usage(),
        "Docker": vm.get_docker_info(),
    }


@app.get("/cpu")
def read_cpu():
    return {"CPU Usage (%)": vm.get_cpu()}
