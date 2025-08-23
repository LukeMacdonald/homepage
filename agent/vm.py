import os
import shutil
import socket
import subprocess

import psutil
from models.docker import Docker
from models.nginx import Nginx
from pydantic import BaseModel


class Virtual_Machine(BaseModel):

    def __init__(self) -> None:
        self._name = socket.gethostname()
        self._ip = ""
        self._docker = Docker()
        self._nginx = Nginx()

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
            "info": self._docker.get_info(),
        }

    def get_nginx_info(self):
        return self._nginx.extract_sites()

    def check_command_exists(self, cmd):
        """Check if a command exists on the system."""
        return shutil.which(cmd) is not None

    def check_service_running(self, service_name):
        """Check if a systemd service is active."""
        try:
            result = subprocess.run(
                ["systemctl", "is-active", "--quiet", service_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return result.returncode == 0
        except FileNotFoundError:
            # systemctl not available (maybe non-systemd OS)
            return False

    def check_process_running(self, process_name):
        """Fallback check using pgrep if systemctl isn't available."""
        try:
            result = subprocess.run(
                ["pgrep", "-x", process_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def is_docker_running(self):
        return self._docker.check_docker()

    def is_kubernetes_running(self):
        # Check kubelet (node) or kubectl (client)
        return self.check_command_exists("kubectl") or self.check_process_running(
            "kubelet"
        )

    def is_nginx_running(self):
        return self.check_service_running("nginx") or self.check_process_running(
            "nginx"
        )

    def is_apache_running(self):
        # Apache service names differ (apache2/httpd)
        return (
            self.check_service_running("apache2")
            or self.check_service_running("httpd")
            or self.check_process_running("apache2")
            or self.check_process_running("httpd")
        )
