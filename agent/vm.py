import os
import socket

import psutil
from models.docker import Docker
from pydantic import BaseModel


class Virtual_Machine(BaseModel):

    def __init__(self) -> None:
        self._name = socket.gethostname()
        self._ip = ""
        self._docker = Docker()

    @property
    def name(self):
        """
        Function to return hostname
        """
        return self._name

    def get_cpu(self):
        """
        Function to obtain CPU usage (%) of host
        """
        return psutil.cpu_percent(interval=1)

    def get_ram(self):
        """
        Function to obtain RAM usage (%) of host
        """
        return psutil.virtual_memory().percent

    def get_disk_usage(self):
        """
        Function to obtain Disk usage (%) of all root directories of host
        """
        paths = os.listdir("/")
        paths = [f"/{path}" for path in paths]
        paths.append("/")
        return [
            {dir: psutil.disk_usage(f"{dir}").percent}
            for dir in paths
            if os.path.isdir(f"{dir}")
        ]

    def get_docker_info(self):
        """
        Function to extract docker information from host
        """
        images, _ = self._docker.get_images()
        containers, _ = self._docker.get_containers()
        return {
            "images": images,
            "containers": containers,
            "data usage": self._docker.get_data_usage(),
            "volumes": self._docker.get_volumes(),
            "networks": self._docker.get_networks(),
        }
